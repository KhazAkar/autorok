import enum
import pathlib
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
    def get_config_options(self, driver: str = 'demo'):
        pass

    @abstractmethod
    def show_connected_devices_details(self, driver: str = 'demo'):
        pass

    @abstractmethod
    def scan_devices(self):
        pass

    @abstractmethod
    def select_measurement_device(self, device: Device):
        pass

    @abstractmethod
    def configure_channels(self,
                           ch_list: typing.List[str],
                           all_ch: bool = False):
        pass

    @abstractmethod
    def configure_measurement(self,
                              wait_for_trigger: bool = False,
                              output_to_file: bool = False,
                              file_type: OutputType = OutputType.CSV,
                              file_path: pathlib.Path = ...):
        pass

    @abstractmethod
    def start_sampled_measurement(self, samples: int, decode: bool = False):
        pass

    @abstractmethod
    def start_framed_measurement(self, frames: int, decode: bool = False):
        pass

    @abstractmethod
    def start_timed_measurement(self, sampling_time: int, decode: bool = False):
        pass
