import pathlib
import enum
import typing
from abc import ABC, abstractmethod
from autorok.devices import Device

class TransformModules(enum.Enum):
    INVERT = 'invert'
    NOP = 'nop'
    SCALE = 'scale'

class InputType(enum.Enum):
    BINARY = 'binary'
    CHRONOVU = 'chronovu'
    CSV = 'csv'
    LOGICPORT = 'logicport'
    NULL = 'null'
    RAW_ANALOG = 'raw_analog'
    TRACE32 = 'trace32_ad'
    VALUE_CHANGE_DUMP = 'vcd'
    WAV = 'wav'

class OutputType(enum.Enum):
    CSV = 'csv'
    ANALOG_ASCII = 'analog'
    ASCII = 'ascii'
    BINARY = 'binary'
    BITS = 'bits'
    CHRONOVU = 'chronovu-la8'
    HEX = 'hex'
    NULL = 'null'
    OLS = 'ols'
    SIGROK_ZIP = 'srzip'
    VALUE_CHANGE_DUMP = 'vcd'
    WAV = 'wav'
    WAVEDROM = 'wavedrom'


class SigrokDriver(ABC):
    @abstractmethod
    def show_connected_devices_details(self):
        pass

    @abstractmethod
    def scan_devices(self):
        pass

    @abstractmethod
    def select_device(self, device: Device):
        pass

    @abstractmethod
    def configure_channels(self, ch: typing.List[str]):
        pass

    @abstractmethod
    def configure_measurement(self, wait_for_trigger: bool = False, output_to_file: bool = False,
                                file_path: pathlib.Path = pathlib.Path('.')):
        pass
    
    @abstractmethod
    def start_sampled_measurement(self, samples: int=0, decode: bool=False):
        pass

    @abstractmethod
    def start_framed_measurement(self, frames: int=0, decode: bool=False):
        pass
