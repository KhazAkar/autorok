import pathlib
import typing
from abc import ABC, abstractmethod
from autorok.devices import Device


class SigrokDriver(ABC):
    @abstractmethod
    def scan_devices(self):
        pass

    @abstractmethod
    def select_device(self, device: Device):
        pass

    @abstractmethod
    def configure_analog_channels(self, ch: typing.List[str]):
        pass

    @abstractmethod
    def configure_digital_channels(self, ch: typing.List[str]):
        pass

    @abstractmethod
    def configure_measurement(self, wait_for_trigger: bool = False, output_to_file: bool = False,
                                file_path: pathlib.Path = pathlib.Path('.')):
        pass
    
    @abstractmethod
    def start_sampled_measurement(self, samples: int=0, decode: bool=False):
        pass
