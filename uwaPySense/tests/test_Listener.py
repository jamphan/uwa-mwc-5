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

    msg_queue = Queue()

    s = SerialTestClass()
    l = Listener(s, msg_queue)
    l.start()

    s.write('test')
    assert msg_queue.empty()
    s.write('stop')