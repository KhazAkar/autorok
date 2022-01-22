import subprocess
import typing
import shutil
from autorok.devices import device_map, Device
from autorok.common import SigrokDriver

class SigrokCLI(SigrokDriver):
    def __init__(self):
        self._active_device: typing.Union[Device, None] = None
        self._detected_devices: typing.Union[typing.Sequence[Device], None] = None
        self._active_analog_channels = ['']
        self._active_digital_channels = ['']

    def configure_analog_channels(self, ch: typing.List[str]):
        self._active_analog_channels = ch
        return self._active_analog_channels
    
    def configure_digital_channels(self, ch: typing.List[str]):
        self._active_digital_channels = ch
        return self._active_digital_channels

    def _gather_devices(self):
        sigrok_path = shutil.which('sigrok-cli')
        sigrok_output = subprocess.run([sigrok_path, '--scan'],
                universal_newlines=True, capture_output=True)
        def _parse_devices():
            output_split = sigrok_output.stdout.split('\n')
            output_split.pop(-1) # Remove trailing newline char
            output_split.pop(0) # Remove first string
            drivers_strings = [driver[:driver.index(' ')] for driver in output_split]  # Gather first part of string, which contains driver 
            ports = []
            for idx, driver in enumerate(drivers_strings):
                if ':' in driver:
                    ports.append((driver[:driver.index(':')], driver[driver.index(':')+1:]))  # create tuple driver,port
                    driver = driver[:driver.index(':')]  # strip :conn from driver name after gathering port
                    drivers_strings[idx] = driver
            for pair in ports:
                device_map[pair[0]].port = pair[1] # assign gathered port to Device instance
            self._detected_devices = [device_map.get(driver, Device('UNKNOWN')) for driver in drivers_strings]
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

