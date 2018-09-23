""" Messages - in this context - is defined as the information that is sent to
the Listener and satisfies certain conditions. In particular the message must
be valid (as dictated by the is_valid()) method, and the series of bytes
on the serial line must be terminated with the specified _end_flag.

"""
import abc
import json

class Msg(object):
    """ This base class ensures three things:
        (1) A default _end_flag is specified
        (2) An abstract method is_valid() is provided
        (3) The data that meets the conditions specified in (1) and (2) is
            stored into a .raw and .as_string property
    """

    def __init__(self):

        self.end_flag = '\n'

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
    def end_flag(self):
        return self._end_flag

    @end_flag.setter
    def end_flag(self, val):
        self._end_flag = bytearray()
        self._end_flag.extend(map(ord, val))

    @property
    def raw(self):

        return self._raw

    @raw.setter
    def raw(self, val):
        self._raw = val
        self._word_len = len(self._raw)
        self._as_string = self._raw[0:self._word_len].decode("utf-8")

    @property
    def as_string(self):
        """ Returns the raw message recieved from the serial line with no
        formatting.
        """

        return self._as_string

# We define a decorated version of the base MSG class to allow users to specify
# their own conditions for a valid message

def default_is_valid(m):

    if len(m.as_string) > 0:
        return True
    else:
        return False

DECORATED_MSG = dict()
DECORATED_MSG['end_flag'] = '\n'
DECORATED_MSG['is_valid'] = default_is_valid

def is_valid(func):
    DECORATED_MSG['is_valid'] = func
    return func

def end_flag(func):
    DECORATED_MSG['end_flag'] = func
    return func

class DecoratedMsg(Msg):
    """ This class is specific to the RF sensors"""

    def __init__(self, *args, **kwargs):

        super(DecoratedMsg, self).__init__(*args, **kwargs)
        self.end_flag = DECORATED_MSG['end_flag'](self)

    def is_valid(self):

        return DECORATED_MSG['is_valid'](self)