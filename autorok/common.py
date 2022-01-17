from abc import ABC, abstractmethod
from autorok.devices import Device

class SigrokDriver(ABC):
    @abstractmethod
    def scan_devices(self):
        pass
    
    @abstractmethod
    def select_device(self, device: Device):
        pass
