import enum
import pathlib
import typing

from autorok.devices import Device
#from autorok.libsigrok import LibSigrok
from autorok.sigrokcli import SigrokCLI


class SigrokInterface(enum.Enum):
    """
    Selector for Sigrok driver to use

    Parameters
    ----------
    enum : SigrokDriver
        Selectable SigrokDriver to use
    """
    SIGROK_CLI = SigrokCLI
    #LIB_SIGROK = LibSigrok


class Autorok:
    """ Main class to use. It's a wrapper which uses LibSigrok or SigrokCLI under the hood, depends on user needs """

    def __init__(self, iface: SigrokInterface):
        self.driver = iface.value()
        self.device_list = list()
        self.active_device: Device = None
        self.active_channels = ['']

    def show_connected_devices_details(self):
        """ Shows details for connected devices, like their options etc """
        return self.driver.show_connected_devices_details()

    def scan_devices(self):
        """ Scans for connected devices,parses them as Device class instances and returns list with them """
        output = self.driver.scan_devices()
        print(f"Following devices were detected: {output}")
        return output

    def select_device(self, device: Device):
        """
        Simple method to select device after scanning

        Parameters
        ----------
        device : Device
            Device instance, taken from scan_devices

        Returns
        -------
        Device
            Currently selected device
        """
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
