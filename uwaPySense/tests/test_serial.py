""" Test class for all serial related matters

Changes:
    2018/09/07: Jamie Phan, Initial version
"""

import pytest
import serial

def main():
    """ Script for individual testing """

    s = SerialTestClass()
    print(type(s.serialPort))

class SerialTestClass(object):
    """ A mock serial port test class"""

    def __init__(self):
        self._port = "loop://"
        self._timeout = 0
        self._baudrate = 115200
        self.serialPort = serial.serial_for_url(url=self._port,
                                                timeout=self._timeout,
                                                baudrate=self._baudrate)

    def write(self, msg):

        msg = msg.encode(encoding='utf-8')
        self.serialPort.write(msg)

    def readline(self):

        return self.serialPort.readline()

    @property
    def in_waiting(self):

        return self.serialPort.in_waiting

    @property
    def is_open(self):

        return self.serialPort.is_open

    def close(self):
        self.serialPort.close()

def test_SerialTestClass():
    """ Test case for the SerialTestClass; make sure we have that configured
    correctly, or the remaining tests will fail
    """

    serialPort = SerialTestClass()

    expected = 'Hello, World!'
    serialPort.write(expected)
    res = serialPort.serialPort.read(len(expected))

    assert res.decode('utf-8') == expected

if __name__ == '__main__':
    main()