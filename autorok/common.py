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
