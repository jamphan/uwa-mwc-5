""" Clients write to database

Changes:
    2018/09/07: Jamie Phan, Initial version
"""

import os
import sys
import abc
import serial
import threading
import time
import queue

from uwaPySense.messages import Msg

class StoppableThread(threading.Thread):
    """ A thread which has flags to determine whether or not it should 
    abruptly be stopped or not. All objects that are derived from this class
    will be stopped when the stop() routine is called by any thread

    Attributes:
        isStopped (bool): Returns TRUE if a stop event was raised
    """

    def __init__(self):

        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._stop_event.clear()

    def stop(self):
        """ This routine will stop all threads of class StoppableThread
        as all classes that are listening to the threading event ._stop_event
        will be set on stop.
        """

        self._stop_event.set()

        try:
            self.clean_up()
        except Exception:
            raise SystemError("Failed to clean up threads cleanly.")

    @abc.abstractmethod
    def clean_up(self):
        """ This method allows derived classes to specify how to clean up their
        processes on a stop event.
        """

        os._exit(0)

    @property
    def isStopped(self):
        """ Checks to see if the event has been set
        """

        return self._stop_event.is_set()

class Listener(StoppableThread):
    """ The Listener is only responsible for listening to messages on the serial
    line and storing them to queue.

    Args:
        serialPort: An open serial port object with read and write methods

    Attributes:
        _serial (serial.serial): The open serial port the object is instantiated
                                 with
        _queue (queue.Queue): This is a shared memory space between this object
                              and the child Worker object. This is the
                              primary method of communication between the 
                              threads
        _worker (Worker): The child thread which must handle all the write 
                          and processing operations

    """

    def __init__(self, serialPort):
        
        super().__init__()

        self._serial = serialPort
        self._queue = queue.Queue()

        self._worker = Worker(self._queue)

    def run(self):
        """ The main loop for the Listener thread. Note this overrides the
        threading.Thread method, and hence will be called upon .start()
        of this thread.
        """

        self._worker.start()

        while not(self.isStopped):

            ser_bytes = self._serial.readline()
            m = Msg(ser_bytes, word_len = len(ser_bytes)-1)

            if m.is_valid():
                self._queue.put_nowait(m)

    def clean_up(self):
        self._worker.stop()
        self._serial.close()

class Worker(StoppableThread):
    """ The worker must write the messages from queue into the database.

    Attributes:
        _queue (queue.Queue): This is a shared memory space between the parent
                              Listener instance and this instance. This is the
                              primary method of communication between the 
                              threads
    """

    def __init__(self, queue):
        
        super().__init__()
        self._queue = queue

    def run(self):
        """ The main loop for the Worker thread. Note this overrides the
        threading.Thread method, and hence will be called upon .start()
        of this thread.
        """

        while not(self.isStopped):

            if not(self._queue.empty()):
                m = self._queue.get_nowait()
                
                # TODO: Replace with actual logic
                # Placeholder
                print(m.as_json)
                # End placeholder

                self._queue.task_done()