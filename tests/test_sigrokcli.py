import pytest
from autorok.autorok import Autorok, SigrokInterface
from autorok.devices import device_map

@pytest.fixture
def sigrok_setup():
    sigrok = Autorok(iface=SigrokInterface.SIGROK_CLI)
    yield sigrok
    del sigrok

def test_should_scan_for_devices(sigrok_setup):
    device_list = sigrok_setup.scan_devices()
    assert device_map.get('demo') in device_list


def test_should_allow_selecting_device(sigrok_setup):
    device_list = sigrok_setup.scan_devices()
    sigrok_setup.select_device(device_list[0])
    assert sigrok_setup.active_device == device_list[0]


def test_should_allow_reconfiguration_of_active_device(sigrok_setup):
    device_list = sigrok_setup.scan_devices()
    sigrok_setup.select_device(device_list[0])
    sigrok_setup.configure_analog_channels(["A0", "A1"])
    sigrok_setup.configure_digital_channels(["D2", "D4"])
    assert sigrok_setup.active_digital_channels == ['D2', 'D4']
    assert sigrok_setup.active_analog_channels == ['A0', 'A1']

def test_should_start_sampled_measurement_wo_decode(sigrok_setup):
    device_list = sigrok_setup.scan_devices()
    sigrok_setup.select_device(device_list[0])
    sigrok_setup.configure_digital_channels(['D0'])
    result = sigrok_setup.start_sampled_measurement(samples=5)
    assert result.returncode == 0 and result.stdout != ''
