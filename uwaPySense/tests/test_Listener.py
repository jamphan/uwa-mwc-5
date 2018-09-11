""" Test class listener class

Changes:
    2018/09/07: Jamie Phan, Initial version
"""

import pytest
import serial
from asyncio import Queue
import time

from tests.test_serial import SerialTestClass
from uwaPySense.Server import Listener

def test_listener():
    """ Check there are no errors
    """

    s = SerialTestClass()

    l = Listener(s)
    l.start()

    s.write('msg:test' + '\n')