import enum
import pathlib
import typing

from autorok.common import OutputType
from autorok.devices import Device
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


class Autorok:
    """ Main class to use. It's a wrapper which uses LibSigrok or SigrokCLI under the hood, depends on user needs """
    def __init__(self, iface: SigrokInterface):
        self.driver = iface.value()
        self.device_list = []
        self.active_device: Device = None
        self.active_channels = ['']

    def show_connected_devices_details(self):
        """ Shows details for connected devices, like their options etc """
        return self.driver.show_connected_devices_details()

    def scan_devices(self):
        """ Scans for connected devices, parses them as Device class instances and returns list with them """
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

    def configure_channels(self,
                           ch_list: typing.List[str],
                           all_ch: bool = False):
        """
        Selects which cnannels should be used for measurement

        Parameters
        ----------
        ch_list : List[str]
            List of channels to be used for measurements
        all_ch : bool
            If true, then all channels are used, by default False
        """
        self.active_channels = self.driver.configure_channels(ch_list, all_ch)

    def configure_measurement(self,
                              wait_for_trigger: bool = False,
                              output_to_file: bool = False,
                              file_type: OutputType = OutputType.CSV,
                              file_path: pathlib.Path = ...):
        """
        Configures measurement. Currently allows for binary output to file with path + waiting for trigger to happen

        Parameters
        ----------
        wait_for_trigger: bool
            Do you want to wait until trigger condition is here? False by default
        output_to_file: bool
            Do you want to record measurement to file? False by default
        file_path: pathlib.Path
            Contains path to the recording file, relative to your $PWD
        """
        self.driver.configure_measurement(wait_for_trigger, output_to_file,
                                          file_type, file_path)

    def start_sampled_measurement(self, samples: int, decode: bool = False):
        """
        Starts measurement counted in samples, using previously configured sampling rate etc.

        Parameters
        ----------
        samples: int
            How many samples do you need?
        decode: bool
            Enables/disables decoding. Disabled (False) by default

        Returns
        -------
        subprocess.CompletedProcess
            Result of measurement with extra metadata
        """
        result = self.driver.start_sampled_measurement(samples=samples,
                                                       decode=decode)
        return result

    def start_framed_measurement(self, frames: int, decode: bool = False):
        """
        Starts measurement counted in frames, using previously configured sampling rate etc.

        Parameters
        ----------
        frames: int
            How many frames do you need?
        decode: bool
            Enables/disables decoding. Disabled (False) by default

        Returns
        -------
        subprocess.CompletedProcess
            Result of measurement with extra metadata
        """
        result = self.driver.start_framed_measurement(frames, decode)
        return result
