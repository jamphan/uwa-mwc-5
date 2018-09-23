import functools
import serial
import time
from datetime import datetime

from . import cli
from . import messages
from .listenerutils import Listener, Worker

class App(object):

    def __init__(self, setup_delay = 0.1):

        self.context = cli.arg_parser()
        self.context.sys.setup_delay = setup_delay
        self._post_setup = list()
        self._setup_success = True
        self.bootup()

    def bootup(self):

        try:
            s = serial.serial_for_url(url=self.context.args.serial_port,
                                      timeout=self.context.args.time_out,
                                      baudrate=self.context.args.baud_rate)
            l = Listener(s, 
                         message_prototype=self.context.args.message_type)
            w = Worker()
            l.set_worker(w)
            time.sleep(self.context.sys.setup_delay)

            self.context.sys.Listener = l
            self.context.sys.SerialPort = s
            self.context.sys.Worker = w
            self.context.WorkRegister = w.get_register()

        except Exception as e:
            self._setup_success = False
            print("System boot failed!\n")
            print(str(e))

    @property
    def addwork(self):
        return self.context.WorkRegister

    @property
    def setup(self):
        """ returns a decorator to allow users to specify what work to 
        add. Functions defined with the returned decrator will be added to
        the registrar, which is called during the operation of the Worker
        thread
        """

        def wrapper_postsetup(func):

            self._post_setup.append(func)
            return func

        return wrapper_postsetup

    def loop(self, rest_time=0.01):
        """ The listener loop is the main loop that the program will sit on
        until a keyboard event stops it. This gives user the option to modify
        the main loop
        """

        def decorator_listenerloop(func):

            @functools.wraps(func)
            def wrapper_listenerloop(*args, **kwargs):
                try:
                    if self._setup_success:
                        self.context.sys.Listener.start()
                    else:
                        raise SystemError("Failed to startup")

                    for post_setup in self._post_setup:
                        post_setup(self.context)

                    while True:
                        time.sleep(rest_time)
                        func(self.context, **kwargs)
                except KeyboardInterrupt:
                    listenerutils.__stop_all_event__.set()
                except Exception as e:
                    listenerutils.__stop_all_event__.set()
                    print("Loop setup failed!\n")
                    print(str(e))

            return wrapper_listenerloop
        return decorator_listenerloop
