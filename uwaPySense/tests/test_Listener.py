""" Unit tests for Listener class
"""

import pytest
import serial
import time
import random
import string

from tests.MessageTestClass import MsgTestClass, MSG_HEAD
from uwaPySense.Server import Listener, Worker

def test_listener_SimpleWriteAndRead(capsys):
    """ Basic test by writing to a serial line (loop:\\) and checking that
    the listener class picks up the correct message
    """

    # Generate the test string
    N = 100
    msg = ''.join(random.choice(string.ascii_letters) for _ in range(N))
    resp_expected = "{}{}\n".format(MSG_HEAD, msg)

    # Initiate all the processes
    s = serial.serial_for_url(url="loop://",
                              timeout=10,
                              baudrate=115200)
    l = Listener(s, message_prototype=MsgTestClass, rest=0.01)
    w = Worker(rest=0.01)
    l.set_worker(w)
    l.start()

    try:
        # Write to the serial line
        # NB. a small delay is required for start up
        s.write(resp_expected.encode('utf-8'))
        time.sleep(0.1) 

        # Capture STDOUT and check the output is as expected
        captured = capsys.readouterr()
        captured_parts = captured.out.split(',')
        resp_actual = captured_parts[1]

        assert resp_expected == resp_actual[:-1] #NB print's add one more line

    except Exception:
        # Something failed
        l.stop()
        assert 1==0 

    l.stop()

def test_listener_BadWriteNoRead(capsys):
    """ Basic test by writing to a serial line (loop:\\) and checking that
    the listener does not pick up any noise
    """

    # Generate the test string
    N = 1000
    msg = ''.join(random.choice(string.ascii_letters) for _ in range(N))
    resp_expected = '{}{}\n'.format('BADHEADER', msg)

    # Initiate all the processes
    s = serial.serial_for_url(url="loop://",
                              timeout=10,
                              baudrate=115200)
    l = Listener(s, message_prototype=MsgTestClass)
    w = Worker()
    l.set_worker(w)
    l.start()

    try:
        # Write to the serial line
        # NB. a small delay is required for start up
        s.write(resp_expected.encode('utf-8'))
        time.sleep(0.1) 

        # Capture STDOUT and check the output is as expected
        captured = capsys.readouterr()
        resp = captured.out

        assert resp == ''

    except Exception:
        # Something failed
        l.stop()
        assert 1==0 

    l.stop()