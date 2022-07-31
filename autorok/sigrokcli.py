import pathlib
import shutil
import subprocess
import typing

from autorok.common import SigrokDriver, OutputType
from autorok.devices import Device, DeviceList


class SigrokCLI(SigrokDriver):
    """ Sigrok driver basing on sigrok-cli Command Line Interface """

    def __init__(self):
        self._active_device: typing.Union[Device, None] = None
        self._detected_devices: typing.Union[typing.Sequence[Device],
                                             None] = None
        self._active_channels = ['']
        self._sigrok_path = shutil.which('sigrok-cli')
        self._sigrok_meas_args = [self._sigrok_path]
        self.measurement_cfg = []
        self._check_sigrok_availability()

    def _check_sigrok_availability(self):
        """
        Checks if sigrok-cli binary is available or not

        Raises
        ------
        ValueError
            No sigrok available - no driver for ya :)
        """
        if self._sigrok_path is None:
            self._sigrok_path = self._sigrok_meas_args[0] = input(
                "Please provide full/absolute path to sigrok executable: ")
            if not self._sigrok_path:
                raise ValueError("No sigrok available, abort.")

    def _get_details(self, driver: str = 'demo'):
        self._check_sigrok_availability()
        details = subprocess.run([self._sigrok_path, '--show', '--driver', driver],
                                 universal_newlines = True,
                                 capture_output = True,
                                 check = True)
        return details

    def _parse_sigrok_config_options(self, details):
        split = details.stdout.splitlines()
        for idx, line in enumerate(split):
            if "Supported configuration options" in line:
                options_idx = idx
        split_cut = split[options_idx + 1:]
        split_cut_stripped = [line.lstrip(' ') for line in split_cut]
        output = {}
        for line in split_cut_stripped:
            if ':' in line:
                split = line.split(': ')
                output[split[0]] = split[1].split(', ')
            if 'samplerate' in line:
                first_space = line.index(' ')
                output[line[:first_space]] = [line[first_space:]]
        return output

    def get_config_options(self, driver: str = 'demo'):
        details = self._get_details(driver = driver)
        output = self._parse_sigrok_config_options(details=details)
        return output

    def show_connected_devices_details(self, driver: str = 'demo'):
        """ Uses subprocess to collect details for connected devices """
        return self._get_details(driver = driver)

    def _cleanup_subprocess_output(self, subprocess_output):
        output_split = subprocess_output.stdout.split('\n')
        output_split.pop(-1)  # Remove trailing newline char
        output_split.pop(0)  # Remove first string
        # Gather first part of string, which contains driver
        drivers_strings = [
            driver[:driver.index(' ')] for driver in output_split
        ]
        return drivers_strings

    def _parse_scan_results(self, subprocess_output):
        drivers_strings = self._cleanup_subprocess_output(subprocess_output)
        for idx, driver in enumerate(drivers_strings):
            if '-' in driver:
                driver = driver.replace('-', '_')
            if ':' in driver:
                # create tuple driver,port
                port = driver[driver.index(':') + 1:]
                # strip :conn from driver name after gathering port and clear out unwanted \n char
                driver = driver[:driver.index(':')]
                getattr(DeviceList, driver).port = port
            drivers_strings[idx] = driver
        self._detected_devices = [
            getattr(DeviceList, driver, Device('UNKNOWN'))
            for driver in drivers_strings
        ]
        return self._detected_devices

    def scan_devices(self):
        self._check_sigrok_availability()
        sigrok_output = subprocess.run([self._sigrok_path, '--scan'],
                                       universal_newlines = True,
                                       capture_output = True,
                                       check = True)

        return self._parse_scan_results(sigrok_output)

    def select_measurement_device(self, device: Device) -> Device:
        """
        Selects device from previously scanned list

        Parameters
        ----------
        device : Device
            Device to be actively used

        Returns
        -------
        Device:
            Active device

        Raises
        ------
        ValueError
            If something other than Device instance was passed, throw exception
        """
        if not isinstance(device, Device):
            raise ValueError("Device class instance should be passed!")
        self._active_device = device
        for elem in ["--driver", device.driver]:
            self._sigrok_meas_args.append(elem)
        return self._active_device

    def configure_channels(self,
                           ch_list: typing.List[str],
                           all_ch: bool = False) -> typing.List:
        """
        Sets active channels for selected driver/device

        Parameters
        ----------
        ch_list: typing.List[str]
            List of channels provided as strings for universality point of view.
        all_ch: bool
            If set to True, it will use all available channels for selected driver/device

        Returns
        -------
        Active selected devices as list
        """
        self._active_channels = [ch_list] if isinstance(ch_list,
                                                        str) else ch_list
        if all_ch:
            self._active_channels = [
                *self._active_device.analog_ch, *self._active_device.digital_ch
            ]
        for elem in ['--channels', ','.join(self._active_channels)]:
            self._sigrok_meas_args.append(elem)

        return self._active_channels

    def configure_measurement(self,
                              wait_for_trigger: bool = False,
                              output_to_file: bool = False,
                              file_type: OutputType = OutputType.CSV,
                              file_path: pathlib.Path = ...) -> None:
        """
        Configures additional stuff to the measurement. Persits between measurements.

        Parameters
        ----------
        wait_for_trigger: bool
            After starting measurement, it should wait until set trigger point, by default False
        output_to_file: bool
            If enabled, it will save measurement results to file, by default False
        file_type: OutputType
            If output_to_file is set to True, it sets type of the output file.
        file_path: pathlib.Path
            Points to the output file
        """
        self.measurement_cfg.clear()
        if wait_for_trigger:
            self.measurement_cfg.append('--wait-trigger')
        if output_to_file:
            for elem in ["--output-file", f"{file_path}", "--output-format", f"{file_type.value}"]:
                self.measurement_cfg.append(elem)
        for elem in self.measurement_cfg:
            self._sigrok_meas_args.append(elem)

    def start_sampled_measurement(self, samples: int, decode: bool = False) -> subprocess.CompletedProcess:
        """
        Starts measurement based on number of samples to gather from device

        Parameters
        ----------
        samples : int
            How many samples to gather from measurement device
        decode : bool
            default:  False
            If true, decoding of measured signals will be performed

        Returns
        -------
        subprocess.CompletedProcess
            Result of measurement with extra metadata

        """
        for elem in ["--samples", str(samples)]:
            self._sigrok_meas_args.append(elem)
        result = subprocess.run(self._sigrok_meas_args,
                                universal_newlines=True,
                                capture_output=True,
                                check=True)
        self._sigrok_meas_args = self._sigrok_meas_args[:-2]
        return result

    def start_framed_measurement(self, frames: int, decode: bool = False) -> subprocess.CompletedProcess:
        """
        Starts measurement, counted in frames

        Parameters
        ----------
        frames: int
            How many frames do you want to collect
        decode: bool
            Do you want to get decoded values or raw ones? False by default
        """
        for elem in ["--frames", str(frames)]:
            self._sigrok_meas_args.append(elem)
        result = subprocess.run(self._sigrok_meas_args,
                                universal_newlines=True,
                                capture_output=True,
                                check=True)
        self._sigrok_meas_args = self._sigrok_meas_args[:-2]
        return result

    def start_timed_measurement(self, sampling_time: int, decode: bool = False) -> subprocess.CompletedProcess:
        """
        """
        for elem in ["--time", str(sampling_time)]:
            self._sigrok_meas_args.append(elem)
        result = subprocess.run(self._sigrok_meas_args,
                                universal_newlines=True,
                                capture_output=True,
                                check=True)
        self._sigrok_meas_args = self._sigrok_meas_args[:-2]
        return result
