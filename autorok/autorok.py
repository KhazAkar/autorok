import enum
import pathlib
import typing
#from autorok.libsigrok import LibSigrok
from autorok.sigrokcli import SigrokCLI
from autorok.devices import Device


class SigrokInterface(enum.Enum):
    SIGROK_CLI = SigrokCLI
    #LIB_SIGROK = LibSigrok


class Autorok:
    def __init__(self, iface: SigrokInterface):
        self.driver = iface.value()
        self.device_list = list()
        self.active_device: Device = None
        self.active_channels = ['']

    def show_connected_devices_details(self):
        return self.driver.show_connected_devices_details()

    def scan_devices(self):
        output = self.driver.scan_devices()
        print(f"Following devices were detected: {output}")
        return output

    def select_device(self, device: Device):
        self.active_device = self.driver.select_device(device)
        return self.active_device

    def configure_channels(self, ch_list: typing.List[str]):
        self.active_channels = self.driver.configure_channels(ch_list)

    def configure_measurement(self, wait_for_trigger: bool = False, output_to_file: bool = False, file_path: pathlib.Path = ...):
        self.driver.configure_measurement(
            wait_for_trigger, output_to_file, file_path)

    def start_sampled_measurement(self, samples: int, decode: bool = False):
        result = self.driver.start_sampled_measurement(samples, decode)
        return result

    def start_framed_measurement(self, frames: int, decode: bool = False):
        result = self.driver.start_framed_measurement(frames, decode)
        return result
