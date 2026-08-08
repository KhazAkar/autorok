"""
Custom exceptions for Autorok.

This module defines all custom exceptions used throughout the Autorok library.
"""


class AutorokError(Exception):
    """Base exception for all Autorok-related errors."""

    pass


class SigrokError(AutorokError):
    """Base exception for sigrok-related errors."""

    pass


class SigrokNotFoundError(SigrokError):
    """Raised when sigrok-cli is not available in the system."""

    pass


class DeviceNotFoundError(SigrokError):
    """Raised when a requested device is not found."""

    pass


class MeasurementError(SigrokError):
    """Raised when a measurement fails."""

    pass


class ConfigurationError(AutorokError):
    """Raised when there is an error in configuration."""

    pass


class InvalidDeviceError(AutorokError):
    """Raised when an invalid device is provided."""

    pass
