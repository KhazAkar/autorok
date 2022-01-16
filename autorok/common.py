from abc import ABC, abstractmethod

class SigrokDriver(ABC):
    @abstractmethod
    def scan_devices(self):
        pass
