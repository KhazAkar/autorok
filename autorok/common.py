"""
Common types and abstract base classes for Autorok.

This module defines the core abstractions and enums used throughout the Autorok library.
"""

import enum
import pathlib
import typing
from abc import ABC, abstractmethod

from autorok.devices import Device


class TransformModules(enum.Enum):
    """Enum for transform modules."""

    INVERT = "invert"
    NOP = "nop"
    SCALE = "scale"


class InputType(enum.Enum):
    """Enum for input types."""

    BINARY = "binary"
    CHRONOVU = "chronovu"
    CSV = "csv"
    LOGICPORT = "logicport"
    NULL = "null"
    RAW_ANALOG = "raw_analog"
    TRACE32 = "trace32_ad"
    VALUE_CHANGE_DUMP = "vcd"
    WAV = "wav"


class OutputType(enum.Enum):
    """Enum for output types."""

    CSV = "csv"
    ANALOG_ASCII = "analog"
    ASCII = "ascii"
    BINARY = "binary"
    BITS = "bits"
    CHRONOVU = "chronovu-la8"
    HEX = "hex"
    NULL = "null"
    OLS = "ols"
    SIGROK_ZIP = "srzip"
    VALUE_CHANGE_DUMP = "vcd"
    WAV = "wav"
    WAVEDROM = "wavedrom"


class SigrokDriver(ABC):
    """Abstract base class for Sigrok drivers."""

    @abstractmethod
    def get_config_options(self, driver: str = "demo") -> dict[str, list[str]]:
        """Get configuration options for a driver."""

    @abstractmethod
    def show_connected_devices_details(
        self, driver: str = "demo"
    ) -> typing.Any:
        """Show details for connected devices."""

    @abstractmethod
    def scan_devices(self) -> list[Device]:
        """Scan for connected devices."""

    @abstractmethod
    def select_measurement_device(self, device: Device) -> Device:
        """Select a measurement device."""

    @abstractmethod
    def configure_channels(
        self, ch_list: list[str] | str, all_ch: bool = False
    ) -> list[str]:
        """Configure channels for measurement."""

    @abstractmethod
    def configure_measurement(
        self,
        wait_for_trigger: bool = False,
        output_to_file: bool = False,
        file_type: OutputType = OutputType.CSV,
        file_path: pathlib.Path | None = None,
    ) -> None:
        """Configure measurement settings."""

    @abstractmethod
    def start_sampled_measurement(
        self, samples: int, decode: bool = False
    ) -> typing.Any:
        """Start a sampled measurement."""

    @abstractmethod
    def start_framed_measurement(
        self, frames: int, decode: bool = False
    ) -> typing.Any:
        """Start a framed measurement."""

    @abstractmethod
    def start_timed_measurement(
        self, sampling_time: int, decode: bool = False
    ) -> typing.Any:
        """Start a timed measurement."""
