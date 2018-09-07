""" Clients write to database

Changes:
    2018/09/07: Jamie Phan, Initial version
"""

import serial
import threading
from asyncio import Queue

from uwaPySense import db
from uwaPySense.messages import MQTTMessage

class StoppableThread(threading.Thread):
    """ A thread which has flags to determine whether or not it should 
    abruptly be stopped or not.

    Args:
        linked_parent (StoppableThread)
    """

    def __init__(self):

        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._linked_obj = None

    def stop(self):
        self._stop_event.set()

    def link_to(self, linked_obj):
        if not(isinstance(linked_obj, StoppableThread)):
            raise TypeError('Linked object for StoppableThreads must be of the same class')

        self._linked_obj = linked_obj

    def isStopped(self):

        if (self._linked_obj is not None and self._linked_obj.isStopped):
            return True
        else:
            return self._stop_event.is_set()

class Listener(StoppableThread):
    """ The Listener is only responsible for listening to messages on the serial
    line and storing them to queue.

    Args:
        serialPort: An open serial port object with read and write methods
        queue (asynio.Queue): A message queue to store messages
    """

    def __init__(self, serialPort, queue):
        
        super().__init__()

        self._serial = serialPort
        self._queue = queue
        
        self._scribe = Scribe(self._queue)
        #self._scribe.link_to(self)

    def run(self):

        self._scribe.start()

        while not(self.isStopped):

            #try:
            ser_bytes = self._serial.readline()
            decoded_bytes =  ser_bytes[0:len(ser_bytes)-2].decode("utf-8")

            m = MQTTMessage(decoded_bytes)
            if m.isAction:
                if m.msg == 'stop':
                    self.stop()

            self._queue.put(m)
            # except:
            #     print("Keyboard Interrupt")
            #     break

class Scribe(StoppableThread):
    """ The scribe must empty the queue into the database. 
    """

    def __init__(self, queue):
        
        super().__init__()
        self._queue = queue

    def run(self):
        """ The main loop"""

        while not(self.isStopped):
            msg_to_write = self._queue.get()
            print(msg_to_write)