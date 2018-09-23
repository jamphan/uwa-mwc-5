import functools
import serial
import time

from . import cli
from . import messages
from .listenerutils import Listener, Worker

SETUP_DELAY = 0.1

def listenerloop(rest_time=0.01, init=None, post_setup=None):

    def decorator_listenerloop(func):
    
        @functools.wraps(func)
        def wrapper_listenerloop(*args, **kwargs):

            ctx = cli.arg_parser()

            try:
                if init is None:
                    s = serial.serial_for_url(url=ctx.serial_port,
                                            timeout=ctx.time_out,
                                            baudrate=ctx.baud_rate)
                    l = Listener(s, message_prototype=ctx.message_type)
                    l.set_worker(Worker())
                    time.sleep(SETUP_DELAY)
                    l.start()
                else:
                    init(ctx, **kwargs)

                if post_setup is not None:
                    post_setup(ctx, **kwargs)

                while True:
                    time.sleep(rest_time)
                    func(ctx, **kwargs)
            except KeyboardInterrupt:
                listenerutils.__stop_all_event__.set()
            except Exception as e:
                listenerutils.__stop_all_event__.set()
                print("Setup failed!\n")
                print(str(e))
        
        return wrapper_listenerloop
    return decorator_listenerloop
