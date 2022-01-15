from abc import ABC, abstractmethod

class SigrokDriver(ABC):
    @abstractmethod
    def _gather_devices(self):
        pass

    @abstractmethod
    def _parse_devices(self):
        pass

    @abstractmethod
    def scan_devices(self):
        pass
