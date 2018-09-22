""" This class is for testing message classes
"""

from uwaPySense.messages import Msg

MSG_HEAD = "testmsg:"

class MsgTestClass(Msg):

    def is_valid(self):

        if self.as_string.startswith(MSG_HEAD):
            return True
        else:
            return False