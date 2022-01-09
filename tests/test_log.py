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
