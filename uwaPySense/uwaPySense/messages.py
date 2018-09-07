import json

class MQTTMessage(object):
    """ A container for MTTQ message frames
    """

    def __init__(self, msg):
        self._msg = msg
        self._isAction = False

    @property
    def msg(self):
        return self._msg

    @property
    def isAction(self):
        return self._isAction

