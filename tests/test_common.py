import pytest
from autorok.common import SigrokInterface, Autorok
from autorok.devices import device_map
def test_should_scan_for_devices():
    sigrok_auto = Autorok(iface=SigrokInterface.SIGROK_CLI)
    device_list = sigrok_auto.scan_devices()
    assert device_map.get('demo') in device_list 

#def test_should_allow_selecting_device():
#    pass
#
#def test_should_provide_measurement_of_desired_signal():
#    pass
#
#def test_should_provide_measurement_of_multiple_signals():
#    pass
#
#def test_should_provide_signal_decoding():
#    pass
#
#def test_should_allow_reconfiguration_of_active_device():
#    pass

