""" Listeners are responsible for listening into the network, capturing all the
data and writing it to file.

The Listener is design to run on a device which is network enabled through
an external device as seen below
     ___________                     ___________
    |           |                   |           |
    | Listener  | <---- USB ------- | Network   |
    |           |                   | device    |
    |___________|                   |___________| 

"""

import sys
import abc
import threading
import queue
import time

import uwaPySense

# This is a global event trigger to stop both the Listener and child-Worker 
# at the same time. Note that the event to stop a StoppableThread is by a
# keyword argument. This gives the option of running independent threads
# that stop on their own accord (e.g. with a delay)
__stop_all_event__ = threading.Event()

class StoppableThread(threading.Thread):
    """ A thread which has flags to determine whether or not it should 
    abruptly be stopped or not. All objects that are derived from this class
    will be stopped when the stop() routine is called by any thread

    Args:
        rest (float): This numeric should be used in the main run() loop as
            a specified time for the thread to 'rest' every iteration
        event (threading.Event): An event, which when set will stop the
            thread. This parameter is a kwarg as some applications may require 
            a global stop event, or conversely may want independent threads

    Attributes:
        isStopped (bool): Returns TRUE if a stop event was raised
    """

    def __init__(self, rest=0.001, event=__stop_all_event__):

        threading.Thread.__init__(self)
        if not(isinstance(event, threading.Event)):
            self._stop_event = threading.Event()
        else:
            self._stop_event = event

        self._stop_event.clear()

        self._rest = rest

    def rest(self):
        """ Resting is essential to ensure that the process does not flood with
        several iterations in the main loop (that is indefinite...)
        """

        if self._rest:
            time.sleep(self._rest)

    def stop(self):
        """ This routine will stop all threads of class StoppableThread
        as all classes that are listening to the threading event ._stop_event
        will be set on stop.

        Raises:
            SystemError: On fail due to .clean_up() method
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
        pass

    @property
    def isStopped(self):
        """ Checks to see if the event has been set
        """

        return self._stop_event.is_set()

class Listener(StoppableThread):
    """ The Listener is only responsible for listening to messages on the serial
    line and storing them to queue. This ensures that the serial TX buffer never
    overflows, or there are no issues with the data stream from the less power-
    -ful device whilst the main thread is busy performing more complex operations
    (such as pushing information to the network)

    Args:
        serialPort (serial.serial): An open serial port object with read and 
            write methods
        message_prototype (uwaPySense.messages.Msg): This is the class prototype
            for the message structure to use. 

    Attributes:
        _queue (queue.Queue): This is a shared memory space between this object
            and the child Worker object. This is the primary method of 
            communication between the threads.
        _worker (Worker): The child thread which must handle all the write 
            and processing operations
    """

    def __init__(self, serialPort, message_prototype, **kwargs):
        
        super(Listener, self).__init__(**kwargs)

        self._serial = serialPort
        self._queue = queue.Queue()
        self._msg_prototype = message_prototype

    def set_worker(self, w):
        """ Set the worker for the listener. This must be set prior to starting
        the Listener thread

        Args:
            w (uwaPySense.Worker): The worker that will perform the complex
                operations for the Listener

        Returns:
            True: On success

        Raises:
            TypeError: When the arg passes is not of type 
                uwaPySense.listenerutils.StoppableThread
        """

        if not(isinstance(w, StoppableThread)):
            raise TypeError("The worker must be of class StoppableThread")
        else:
            self._worker = w
            self._worker.assign_to(self._queue)

        return True

    def run(self):
        """ The main loop for the Listener thread. Note this overrides the
        threading.Thread method, and hence will be called upon .start()
        of this thread.

        Raises:
            SystemError: if there is no Worker assigned to the thread
        """

        if self._worker is None:
            raise SystemError("No worker assigned to Listener. Cannot start the thread!")
        else:
            self._worker.start()

        while not(self.isStopped):
            
            m = self._msg_prototype()
            m.raw = self._serial.read_until(m.end_flag)

            if m.is_valid():
                self._queue.put_nowait(m)
            
            self.rest()

    def clean_up(self):
        """ Final clean up when the thread stops
        """

        self._worker.stop()
        self._serial.close()

class Worker(StoppableThread):
    """ Responsible for acting on messages recieved by the Listener

    Attributes:
        _registrar (list): A list of functions that the worker is to
            perform on the queue items. If this list blank, the messages
            are are taken out of queue and ultimately lost.
    """

    def __init__(self, **kwargs):
        
        super(Worker, self).__init__(**kwargs)
        self._registrar = list()

    def assign_to(self, q):
        """ Assign the worker to a queue to act on

        Args:
            _queue (queue.Queue): This is a shared memory space between the 
                parent Listener instance and this instance. This is the
                primary method of communication between the threads

        Raises:
            TypeError: If the argument passed is not of type queue.Queue
        """

        if not(isinstance(q, queue.Queue)):
            raise TypeError("Workers can only work on queue.Queue types")
        else:
            self._queue = q

    def get_register(self):
        """ returns a decorator to allow users to specify what work to 
        add. Functions defined with the returned decrator will be added to
        the registrar, which is called during the operation of the Worker
        thread
        """

        def wrapper_registrar(func):
            self._registrar.append(func)
            return func

        return wrapper_registrar

    def run(self):
        """ The main loop for the Worker thread. Note this overrides the
        threading.Thread method, and hence will be called upon .start()
        of this thread.
        """

        while not(self.isStopped):

            if not(self._queue.empty()):
                m = self._queue.get_nowait()

                for work in self._registrar:
                    work(m)

                self._queue.task_done()
            
            self.rest()