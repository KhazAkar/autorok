import pathlib
import re
import shutil
import subprocess
import time

from autorok.common import OutputType, SigrokDriver
from autorok.devices import Device, DeviceList
from autorok.exceptions import (
    ConfigurationError,
    InvalidDeviceError,
    SigrokNotFoundError,
)


class SigrokCLI(SigrokDriver):
    """Sigrok driver basing on sigrok-cli Command Line Interface."""

    def __init__(self) -> None:
        self._active_device: Device | None = None
        self._detected_devices: list[Device] | None = None
        self._active_channels: list[str] = [""]
        self._sigrok_path = shutil.which("sigrok-cli")
        self._sigrok_meas_args: list[str] = [self._sigrok_path] if self._sigrok_path else []
        self.measurement_cfg: list[str] = []
        self._scan_cache: list[Device] | None = None
        self._scan_cache_time: float = 0.0
        self._scan_cache_ttl: float = 5.0  # seconds
        self._check_sigrok_availability()

    def _check_sigrok_availability(self) -> None:
        """
        Checks if sigrok-cli binary is available or not.

        Raises
        ------
        SigrokNotFoundError
            No sigrok available.
        """
        if self._sigrok_path is None:
            self._sigrok_path = input("Please provide full/absolute path to sigrok executable: ")
            if not self._sigrok_path:
                raise SigrokNotFoundError("No sigrok available, abort.")
            self._sigrok_meas_args = [self._sigrok_path]

    def _get_details(self, driver: str = "demo") -> subprocess.CompletedProcess[str]:
        self._check_sigrok_availability()
        details = subprocess.run(
            [self._sigrok_path, "--show", "--driver", driver],
            capture_output=True,
            check=True,
            text=True,
        )
        return details

    def _parse_sigrok_config_options(self, details: subprocess.CompletedProcess[str]) -> dict[str, list[str]]:
        split = details.stdout.splitlines()
        for idx, line in enumerate(split):
            if "Supported configuration options" in line:
                options_idx = idx
                break
        else:
            return {}

        split_cut = split[options_idx + 1 :]
        split_cut_stripped = [line.lstrip(" ") for line in split_cut]
        output: dict[str, list[str]] = {}
        for line in split_cut_stripped:
            if ":" in line:
                split_line = line.split(": ")
                output[split_line[0]] = split_line[1].split(", ")
            if "samplerate" in line:
                first_space = line.index(" ")
                output[line[:first_space]] = [line[first_space:]]
        return output

    def get_config_options(self, driver: str = "demo") -> dict[str, list[str]]:
        details = self._get_details(driver=driver)
        output = self._parse_sigrok_config_options(details=details)
        return output

    def show_connected_devices_details(self, driver: str = "demo") -> subprocess.CompletedProcess[str]:
        """Uses subprocess to collect details for connected devices."""
        return self._get_details(driver=driver)

    def _cleanup_subprocess_output(self, subprocess_output: subprocess.CompletedProcess[str]) -> list[str]:
        output_split = subprocess_output.stdout.split("\n")
        if output_split:
            output_split.pop(-1)  # Remove trailing newline char
        if output_split:
            output_split.pop(0)  # Remove first string
        # Gather first part of string, which contains driver
        drivers_strings = [driver[: driver.index(" ")] for driver in output_split]
        return drivers_strings

    def _parse_scan_results(self, subprocess_output: subprocess.CompletedProcess[str]) -> list[Device]:
        """Parse sigrok-cli scan output more robustly."""
        drivers_strings: list[str] = []
        device_pattern = re.compile(r"^([a-z0-9_-]+)(?::([a-z0-9/-]+))?")

        lines = subprocess_output.stdout.strip().split("\n")
        for line in lines[1:]:  # Skip header
            line = line.strip()
            if not line:
                continue

            match = device_pattern.match(line)
            if match:
                driver_name = match.group(1).replace("-", "_")
                port = match.group(2) or ""

                if hasattr(DeviceList, driver_name):
                    device = getattr(DeviceList, driver_name)
                    device.port = port
                    drivers_strings.append(device)
                else:
                    drivers_strings.append(Device(driver_name, port))

        self._detected_devices = drivers_strings
        return self._detected_devices

    def scan_devices(self) -> list[Device]:
        """Scan for connected devices with caching."""
        current_time = time.time()
        if self._scan_cache is not None and (current_time - self._scan_cache_time) < self._scan_cache_ttl:
            return self._scan_cache

        self._check_sigrok_availability()
        sigrok_output = subprocess.run(
            [self._sigrok_path, "--scan"],
            capture_output=True,
            check=True,
            text=True,
        )

        result = self._parse_scan_results(sigrok_output)
        self._scan_cache = result
        self._scan_cache_time = current_time
        return result

    def select_measurement_device(self, device: Device) -> Device:
        """
        Selects device from previously scanned list.

        Parameters
        ----------
        device : Device
            Device to be actively used.

        Returns
        -------
        Device:
            Active device.

        Raises
        ------
        InvalidDeviceError
            If something other than Device instance was passed, or device not in scanned list.
        """
        if not isinstance(device, Device):
            raise InvalidDeviceError("Device class instance should be passed!")

        if self._detected_devices and device not in self._detected_devices:
            raise InvalidDeviceError(f"Device {device} was not found in scanned devices list")

        self._active_device = device
        self._sigrok_meas_args = [self._sigrok_path, "--driver", device.driver]
        return self._active_device

    def configure_channels(self, ch_list: list[str] | str, all_ch: bool = False) -> list[str]:
        """
        Sets active channels for selected driver/device.

        Parameters
        ----------
        ch_list: list[str] | str
            List of channels provided as strings for universality point of view.
        all_ch: bool
            If set to True, it will use all available channels for selected driver/device.

        Returns
        -------
        Active selected devices as list.
        """
        if isinstance(ch_list, str):
            self._active_channels = [ch_list]
        else:
            self._active_channels = ch_list

        if all_ch:
            analog = self._active_device.analog_ch or []
            digital = self._active_device.digital_ch or []
            self._active_channels = [*analog, *digital]

        self._sigrok_meas_args.extend(["--channels", ",".join(self._active_channels)])
        return self._active_channels

    def configure_measurement(
        self,
        wait_for_trigger: bool = False,
        output_to_file: bool = False,
        file_type: OutputType = OutputType.CSV,
        file_path: pathlib.Path | None = None,
    ) -> None:
        """
        Configures additional stuff to the measurement. Persists between measurements.

        Parameters
        ----------
        wait_for_trigger: bool
            After starting measurement, it should wait until set trigger point.
        output_to_file: bool
            If enabled, it will save measurement results to file.
        file_type: OutputType
            If output_to_file is set to True, it sets type of the output file.
        file_path: pathlib.Path | None
            Points to the output file.

        Raises
        ------
        ConfigurationError
            If output_to_file is True but file_path is None.
        """
        self.measurement_cfg.clear()

        if wait_for_trigger:
            self.measurement_cfg.append("--wait-trigger")

        if output_to_file:
            if file_path is None:
                raise ConfigurationError("file_path must be provided when output_to_file is True")
            self.measurement_cfg.extend(["--output-file", str(file_path), "--output-format", file_type.value])

        self._sigrok_meas_args.extend(self.measurement_cfg)

    def _build_measurement_command(self, measurement_arg: str, value: int) -> list[str]:
        """Build the complete measurement command from current configuration."""
        cmd = self._sigrok_meas_args.copy()
        cmd.extend([measurement_arg, str(value)])
        return cmd

    def start_sampled_measurement(self, samples: int, decode: bool = False) -> subprocess.CompletedProcess[str]:
        """
        Starts measurement based on number of samples to gather from device.

        Parameters
        ----------
        samples : int
            How many samples to gather from measurement device.
        decode : bool
            If true, decoding of measured signals will be performed.

        Returns
        -------
        subprocess.CompletedProcess
            Result of measurement with extra metadata.
        """
        cmd = self._build_measurement_command("--samples", samples)
        if decode:
            cmd.append("--decode")

        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            text=True,
        )
        return result

    def start_framed_measurement(self, frames: int, decode: bool = False) -> subprocess.CompletedProcess[str]:
        """
        Starts measurement, counted in frames.

        Parameters
        ----------
        frames: int
            How many frames do you want to collect.
        decode: bool
            Do you want to get decoded values or raw ones? False by default.
        """
        cmd = self._build_measurement_command("--frames", frames)
        if decode:
            cmd.append("--decode")

        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            text=True,
        )
        return result

    def start_timed_measurement(self, sampling_time: int, decode: bool = False) -> subprocess.CompletedProcess[str]:
        """
        Starts measurement for X amount of time (in seconds).

        Parameters
        ----------
        sampling_time: int
            How long do you want to record data? (in seconds).
        decode: bool
            Enables/disables decoding. Disabled (False) by default.
        """
        cmd = self._build_measurement_command("--time", sampling_time)
        if decode:
            cmd.append("--decode")

        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            text=True,
        )
        return result
