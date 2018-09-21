import json

class Msg(object):

    def __init__(self, bytes_read, word_len = 8):

        self._raw = bytes_read[0:word_len].decode("utf-8")

    @property
    def raw(self):
        """ Returns the raw message recieved from the serial line with no 
        formatting.
        """

        # TODO: Replace with actual logic
        # Placeholder
        return self._raw
        # End placeholder

    @property
    def as_json(self):
        """ Formats the message in the JSON format required for the NoSQL db
        """

        # TODO: Replace with actual logic
        # Placeholder
        return self._raw
        # End placeholder

    def is_valid(self):
        """ Checks to see the message recieved is correct
        """

        # TODO: Replace with actual logic
        # Placeholder
        if self._raw.startswith('msg:'):
            return True
        else:
            return False
        # End placeholder

class RfMsg(Msg):
    """ This class is specific to the RF sensors"""

    def __init__(self, *args, **kwargs):

        super(RfMsg, self).__init__(*args, **kwargs)

    def is_valid(self):

        if len(self._raw) > 0 and self._raw[0].isdigit():
            return True
        else:
            return False