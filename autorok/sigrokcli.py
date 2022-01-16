import subprocess
import shutil
from autorok.devices import device_map, Device
from autorok.common import SigrokDriver

class SigrokCLI(SigrokDriver):
    def _gather_devices(self):
        sigrok_path = shutil.which('sigrok-cli')
        sigrok_output = subprocess.run([sigrok_path, '--scan'],
                universal_newlines=True, capture_output=True)
        def _parse_devices():
            output_split = sigrok_output.stdout.split('\n')
            output_split.pop(-1) # Remove trailing newline char
            output_split.pop(0) # Remove first string
            drivers_strings = [driver[:driver.index(' ')] for driver in output_split]
            drivers = [device_map.get(driver, Device('UNKNOWN')) for driver in drivers_strings]
            return drivers
        return _parse_devices()

    def scan_devices(self):
        result = self._gather_devices()
        print("Following devices were found: {result}")
        return result
