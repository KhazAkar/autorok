import enum
#from autorok.libsigrok import LibSigrok
from autorok.sigrokcli import SigrokCLI
from autorok.devices import Device, device_map

class SigrokInterface(enum.Enum):
    SIGROK_CLI = SigrokCLI
    #LIB_SIGROK = LibSigrok

class Autorok:
    def __init__(self, iface: SigrokInterface):
       self.driver = iface.value()
       self.device_list = list()
       self.active_device: Device = None

    def scan_devices(self):
        output = self.driver.scan_devices()
        print(f"Following devices were detected: {output}")
        return output

    def select_device(self, device: Device):
        self.active_device = self.driver.select_device(device)
        return self.active_device
