import functools
import serial
import time
from datetime import datetime

from . import cli
from . import messages
from .listenerutils import Listener, Worker

SETUP_DELAY = 0.1

class App(object):

    def __init__(self):

        self.context = cli.arg_parser()
        self._post_setup = list()
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
            time.sleep(SETUP_DELAY)

            self.context.sys.Listener = l
            self.context.sys.SerialPort = s
            self.context.sys.Worker = w
            self.context.WorkRegister = w.get_register()

            if self.context.args.output_file is not None:
                open(self.context.args.output_file, 'w').close()

                @self.context.WorkRegister
                def _(m):
                    now = datetime.now()

                    with open(self.context.args.output_file, 'a') as fh:
                        fh.write("[{}]:\t{}\n".format(now, m.as_string))

        except Exception as e:
            listenerutils.__stop_all_event__.set()
            print("System boot failed!\n")
            print(str(e))

        self.context.sys.Listener.start()

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
                    for post_setup in self._post_setup:
                        post_setup(self.context)

                    while True:
                        time.sleep(rest_time)
                        func(self.context, **kwargs)
                except KeyboardInterrupt:
                    listenerutils.__stop_all_event__.set()

            return wrapper_listenerloop
        return decorator_listenerloop
