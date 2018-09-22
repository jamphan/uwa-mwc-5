import abc
import json

def to_bytes(seq):
    """convert a sequence to a bytes type"""
    if isinstance(seq, bytes):
        return seq
    elif isinstance(seq, bytearray):
        return bytes(seq)
    elif isinstance(seq, memoryview):
        return seq.tobytes()
    elif isinstance(seq, str):
        raise TypeError('unicode strings are not supported, please encode to bytes: {!r}'.format(seq))
    else:
        # handle list of integers and bytes (one or more items) for Python 2 and 3
        return bytes(bytearray(seq))

class Msg(object):

    _end_flag = bytearray()
    _end_flag.extend(map(ord, '\n'))

    def __init__(self, bytes_in, word_len=8):

        self._raw = bytes_in
        self._word_len = word_len

        self._as_string = self._raw[0:self._word_len].decode("utf-8")

    @abc.abstractmethod
    def is_valid(self):
        """ Determine if the message read is a valid message that follows
        the desired protocol or not.

        This method must return True when the message is valid, and False
        when the message is an invalid message - either due to a
        transmission errors, or not following the required format.
        """

        pass

    @property
    def as_string(self):
        """ Returns the raw message recieved from the serial line with no 
        formatting.
        """

        return self._as_string

    @property
    def as_json(self):
        """ Formats the message in the JSON format required for the NoSQL db
        """

        return self._raw

class RFMsg(Msg):
    """ This class is specific to the RF sensors"""

    _end_flag = bytearray()
    _end_flag.extend(map(ord, 'END'))

    def is_valid(self):

        if len(self.as_string) > 0 and self.as_string[0].isdigit():
            return True
        else:
            return False

    @property
    def as_json(self):

        col_RRSI = 10

        msg_parts = [float(x) for x in self.as_string.split(',')]
        try:
            return str(msg_parts[col_RRSI])
        except IndexError:
            return None