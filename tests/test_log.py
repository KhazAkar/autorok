#
# TDD part of AMDD learning excercise, #1 Use Case - Set logging
#
import pytest
from autorok.log import Log


def test_should_enable_logging():
    log = Log()
    log.enable_logging()
    assert log.status == True
    del log


def test_should_disable_logging():
    log = Log()
    log.disable_logging()
    assert log.status == False
    del log

def test_should_provide_default_configuration():
    log = Log()
    log.enable_logging()
    assert len(log.live_cfg) > 1
    del log

#def test_should_load_config_from_file():
#    pass
#
#def test_should_configure_onthefly():
#    pass
#
#def test_should_allow_configure_msg_format():
#    pass
#
#def test_should_allow_configure_log_output_dst():
#    pass
