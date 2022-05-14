import os
import pathlib

import pytest

from autorok.common import OutputType
from autorok.autorok import Autorok, SigrokInterface
from autorok.devices import device_map


@pytest.fixture
def sigrok():
    sigrok_obj = Autorok(iface=SigrokInterface.SIGROK_CLI)
    yield sigrok_obj
    del sigrok_obj


def test_should_scan_for_devices(sigrok):
    device_list = sigrok.scan_devices()
    assert device_map.get('demo') in device_list


def test_should_allow_selecting_device(sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    assert sigrok.active_device == device_list[0]


def test_should_allow_reconfiguration_of_active_device(sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    sigrok.configure_channels(["A0", "A1", "D2", "D3"])
    assert sigrok.active_channels == ["A0", "A1", "D2", "D3"]


def test_should_show_detailed_devices_information(sigrok):
    result = sigrok.show_connected_devices_details()
    assert result.returncode == 0 and result.stdout != ''


def test_should_start_sampled_measurement_wo_decode(sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    sigrok.configure_channels(['D0'])
    result = sigrok.start_sampled_measurement(samples=5)
    assert result.returncode == 0 and result.stdout != ''


def test_should_start_framed_measurement_wo_decode(sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    sigrok.configure_channels(['D1', 'A2'])
    result = sigrok.start_framed_measurement(frames=2)
    assert result.returncode == 0 and result.stdout != ''


def test_should_start_time_based_measurement_wo_decode(sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    sigrok.configure_channels(['D0', 'A1'])
    result = sigrok.start_timed_measurement(sampling_time = 2)
    assert result.returncode == 0 and result.stdout != ''


def test_should_record_result_to_file_from_measurement(sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    sigrok.configure_channels(['D0'])
    file = pathlib.Path('test_measurement_22.22.22.log')
    sigrok.configure_measurement(output_to_file=True, file_path=file)
    sigrok.start_sampled_measurement(2)
    assert os.path.isfile(file)
    os.remove(file)


def test_should_record_result_to_file_from_measurement_with_selected_output_file_type(
        sigrok):
    device_list = sigrok.scan_devices()
    sigrok.select_device(device_list[0])
    sigrok.configure_channels(['D0', 'D1'])
    file = pathlib.Path('test_measurement_33.33.34.vcd')
    sigrok.configure_measurement(output_to_file=True,
                                 file_type=OutputType.VALUE_CHANGE_DUMP,
                                 file_path=file)
    sigrok.start_sampled_measurement(2)
    assert os.path.isfile(file)
    os.remove(file)
