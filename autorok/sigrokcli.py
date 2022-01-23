import pathlib
import subprocess
import typing
import datetime
import shutil
from autorok.devices import device_map, Device
from autorok.common import SigrokDriver


class SigrokCLI(SigrokDriver):
    def __init__(self):
        self._active_device: typing.Union[Device, None] = None
        self._detected_devices: typing.Union[typing.Sequence[Device], None] = None
        self._active_analog_channels = ['']
        self._active_digital_channels = ['']
        self._sigrok_path = shutil.which('sigrok-cli')
        self.measurement_cfg = list()

    def configure_analog_channels(self, ch: typing.List[str]):
        self._active_analog_channels = [ch] if type(ch) == str else ch
        return self._active_analog_channels

    def configure_digital_channels(self, ch: typing.List[str]):
        self._active_digital_channels = [ch] if type(ch) == str else ch
        return self._active_digital_channels

    def _gather_devices(self):
        sigrok_output = subprocess.run([self._sigrok_path, '--scan'],
                universal_newlines=True, capture_output=True)

        def _parse_devices():
            output_split = sigrok_output.stdout.split('\n')
            output_split.pop(-1)  # Remove trailing newline char
            output_split.pop(0)  # Remove first string
            # Gather first part of string, which contains driver
            drivers_strings = [
                driver[:driver.index(' ')] for driver in output_split]
            ports = []
            for idx, driver in enumerate(drivers_strings):
                if ':' in driver:
                    # create tuple driver,port
                    ports.append(
                        (driver[:driver.index(':')], driver[driver.index(':')+1:]))
                    # strip :conn from driver name after gathering port and clear out unwanted \n char
                    driver = driver[:driver.index(':')]
                    drivers_strings[idx] = driver
            for pair in ports:
                # assign gathered port to Device instance
                device_map[pair[0]].port = pair[1]
            self._detected_devices = [device_map.get(
                driver, Device('UNKNOWN')) for driver in drivers_strings]
            return self._detected_devices
        return _parse_devices()

    def scan_devices(self):
        result = self._gather_devices()
        return result

    def select_device(self, device: Device):
        if not isinstance(device, Device):
            raise ValueError("Device class instance should be passed!")
        self._active_device = device
        return self._active_device

    def configure_measurement(self, wait_for_trigger: bool = False, output_to_file: bool = False, file_path: pathlib.Path = ...):
        self.measurement_cfg.clear()
        if wait_for_trigger:
            self.measurement_cfg.append('--wait-trigger')
        if output_to_file:
            curr_time = datetime.datetime.now()
            self.measurement_cfg.append(f'--output-file {file_path}_{curr_time.year}-{curr_time.month}-{curr_time.day}-{curr_time.hour}-{curr_time.minute}-{curr_time.second}.log') 
    
    def start_sampled_measurement(self, samples: int):
        args = [self._sigrok_path, "--driver", self._active_device.driver, "--samples", str(samples), '--channels']
        active_ch = [*self._active_analog_channels, *self._active_digital_channels]
        if active_ch:
            args.append(",".join(active_ch).strip(','))
        else:
            args.append(",".join([*self._active_device.analog_ch, *self._active_device.digital_ch]))
        if self.measurement_cfg:
            args.append(" ".join(self.measurement_cfg))
        result = subprocess.run(args, universal_newlines=True, capture_output=True)
        return result