"""Tests for the SigrokCLI driver."""

import os
import pathlib

import pytest

from autorok.autorok import Autorok, SigrokInterface
from autorok.common import OutputType
from autorok.devices import Device
from autorok.exceptions import ConfigurationError, InvalidDeviceError


@pytest.fixture
def sigrok():
    """Fixture providing an Autorok instance with SigrokCLI driver."""
    sigrok_obj = Autorok(iface=SigrokInterface.SIGROK_CLI)
    yield sigrok_obj
    del sigrok_obj


def test_should_scan_for_devices(sigrok):
    """Test that scan_devices returns a list of Device instances."""
    device_list = sigrok.scan_devices()
    assert isinstance(device_list[-1], Device)


def test_should_allow_selecting_device(sigrok):
    """Test selecting a device from the scanned list."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    assert sigrok.active_device == device_list[0]


def test_should_allow_reconfiguration_of_active_device(sigrok):
    """Test reconfiguring channels on the active device."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["A0", "A1", "D2", "D3"])
    assert sigrok.active_channels == ["A0", "A1", "D2", "D3"]


def test_should_show_detailed_devices_information(sigrok):
    """Test showing detailed device information."""
    result = sigrok.show_connected_devices_details()
    assert result.returncode == 0 and result.stdout != ""


def test_should_start_sampled_measurement_wo_decode(sigrok):
    """Test starting a sampled measurement without decode."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["D0"])
    result = sigrok.start_sampled_measurement(samples=5)
    assert result.returncode == 0 and result.stdout != ""


def test_should_allow_measurement_rerun(sigrok):
    """Test rerunning a measurement with different parameters."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["D0"])
    sigrok.start_sampled_measurement(samples=2)
    result = sigrok.start_framed_measurement(frames=3)
    assert result.returncode == 0 and result.stdout != "" and "--samples" not in result.args


def test_should_start_framed_measurement_wo_decode(sigrok):
    """Test starting a framed measurement without decode."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["D1", "A2"])
    result = sigrok.start_framed_measurement(frames=2)
    assert result.returncode == 0 and result.stdout != ""


def test_should_start_time_based_measurement_wo_decode(sigrok):
    """Test starting a time-based measurement without decode."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["D0", "A1"])
    result = sigrok.start_timed_measurement(sampling_time=2)
    assert result.returncode == 0 and result.stdout != ""


def test_should_record_result_to_file_from_measurement(sigrok):
    """Test recording measurement results to a file."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["D0"])
    file_path = pathlib.Path("test_measurement_22.22.22.log")
    sigrok.configure_measurement(output_to_file=True, file_path=file_path)
    sigrok.start_sampled_measurement(2)
    assert os.path.isfile(file_path)
    os.remove(file_path)


def test_should_record_result_to_file_from_measurement_with_selected_output_file_type(
    sigrok,
):
    """Test recording measurement results to a file with a specific output type."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    sigrok.configure_channels(["D0", "D1"])
    file_path = pathlib.Path("test_measurement_33.33.34.vcd")
    sigrok.configure_measurement(
        output_to_file=True,
        file_type=OutputType.VALUE_CHANGE_DUMP,
        file_path=file_path,
    )
    sigrok.start_sampled_measurement(2)
    assert os.path.isfile(file_path)
    os.remove(file_path)


def test_should_show_available_config_options(sigrok):
    """Test showing available configuration options."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    config_options = sigrok.get_config_options()
    assert config_options.get("samplerate", None) is not None


def test_should_raise_error_for_invalid_device(sigrok):
    """Test that selecting an invalid device raises an error."""
    with pytest.raises(InvalidDeviceError):
        sigrok.select_measurement_device("not a device")


def test_should_raise_error_for_config_without_file_path(sigrok):
    """Test that configuring output to file without a path raises an error."""
    device_list = sigrok.scan_devices()
    sigrok.select_measurement_device(device_list[0])
    with pytest.raises(ConfigurationError):
        sigrok.configure_measurement(output_to_file=True, file_path=None)
