from autorok.common import SigrokDriver
from autorok.devices import Device, device_map

class Autorok:
    def __init__(self, driver: SigrokDriver):
       self.driver = driver 

    def scan_devices(self):
        output = self.driver.scan_devices()
        print(f"Following devices were detected: {output}")
        return output
