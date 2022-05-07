import pathlib
import shutil
import subprocess
import typing

from autorok.common import SigrokDriver, OutputType
from autorok.devices import Device, device_map


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

    def _handle_sigrok_args(self):
        """
        Parser for sigrok arguments - flattens the list basically.
        """
        temp = self._sigrok_meas_args.copy()
        self._sigrok_meas_args.clear()
        for elem in temp:
            if isinstance(elem, list):
                for inner_elem in elem:
                    self._sigrok_meas_args.append(inner_elem)
            else:
                self._sigrok_meas_args.append(elem)

    def show_connected_devices_details(self):
        """ Uses subprocess to collect details for connected devices """
        self._check_sigrok_availability()
        sigrok_output = subprocess.run([self._sigrok_path, '--show'],
                                       check=True)
        return sigrok_output

    def scan_devices(self):
        self._check_sigrok_availability()
        sigrok_output = subprocess.run([self._sigrok_path, '--scan'],
                                       universal_newlines=True,
                                       capture_output=True,
                                       check=True)

        def _parse_devices():
            output_split = sigrok_output.stdout.split('\n')
            output_split.pop(-1)  # Remove trailing newline char
            output_split.pop(0)  # Remove first string
            # Gather first part of string, which contains driver
            drivers_strings = [
                driver[:driver.index(' ')] for driver in output_split
            ]
            ports = []
            for idx, driver in enumerate(drivers_strings):
                if ':' in driver:
                    # create tuple driver,port
                    ports.append((driver[:driver.index(':')],
                                  driver[driver.index(':') + 1:]))
                    # strip :conn from driver name after gathering port and clear out unwanted \n char
                    driver = driver[:driver.index(':')]
                    drivers_strings[idx] = driver
            for pair in ports:
                # assign gathered port to Device instance
                device_map[pair[0]].port = pair[1]
            self._detected_devices = [
                device_map.get(driver, Device('UNKNOWN'))
                for driver in drivers_strings
            ]
            return self._detected_devices

        return _parse_devices()

    def select_device(self, device: Device):
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
        self._sigrok_meas_args.append(["--driver", device.driver])
        return self._active_device

    def configure_channels(self, ch: typing.List[str], all_ch: bool = False):
        self._active_channels = [ch] if isinstance(ch, str) else ch
        if all_ch:
            self._active_channels = [
                *self._active_device.analog_ch, *self._active_device.digital_ch
            ]
        self._sigrok_meas_args.append(
            ['--channels', ','.join(self._active_channels)])
        return self._active_channels

    def configure_measurement(self,
                              wait_for_trigger: bool = False,
                              output_to_file: bool = False,
                              file_type: OutputType = OutputType.CSV,
                              file_path: pathlib.Path = ...):
        self.measurement_cfg.clear()
        if wait_for_trigger:
            self.measurement_cfg.append('--wait-trigger')
        if output_to_file:
            self.measurement_cfg.append(["--output-file", f"{file_path}"])
            self.measurement_cfg.append(
                ["--output-format", f"{file_type.value}"])

    def start_sampled_measurement(self, samples: int, decode: bool = False):
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
        if self.measurement_cfg:
            for elem in self.measurement_cfg:
                self._sigrok_meas_args.append(elem)
        self._sigrok_meas_args.append(["--samples", str(samples)])
        self._handle_sigrok_args()
        result = subprocess.run(self._sigrok_meas_args,
                                universal_newlines=True,
                                capture_output=True,
                                check=True)
        return result

    def start_framed_measurement(self, frames: int, decode: bool = False):
        if self.measurement_cfg:
            self._sigrok_meas_args.append(" ".join(self.measurement_cfg))
        self._sigrok_meas_args.append(["--frames", str(frames)])
        self._handle_sigrok_args()
        result = subprocess.run(self._sigrok_meas_args,
                                universal_newlines=True,
                                capture_output=True,
                                check=True)
        return result
