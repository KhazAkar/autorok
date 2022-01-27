import pytest
from autorok.autorok import Autorok, SigrokInterface
from autorok.devices import device_map


@pytest.fixture
def sigrok():
    sigrok = Autorok(iface=SigrokInterface.SIGROK_CLI)
    yield sigrok
    del sigrok


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
