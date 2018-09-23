import functools
import serial
import time
from datetime import datetime

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
                    s = serial.serial_for_url(url=ctx.args.serial_port,
                                            timeout=ctx.args.time_out,
                                            baudrate=ctx.args.baud_rate)
                    l = Listener(s, message_prototype=ctx.args.message_type)
                    w = Worker()
                    l.set_worker(w)
                    time.sleep(SETUP_DELAY)

                    ctx.sys.Listener = l
                    ctx.sys.SerialPort = s
                    ctx.sys.Worker = w
                    ctx.WorkRegister = w.get_register()

                    if ctx.args.output_file is not None:
                        open(ctx.args.output_file, 'w').close()

                        @ctx.WorkRegister
                        def _(m):
                            now = datetime.now()

                            with open(ctx.args.output_file, 'a') as fh:
                                fh.write("[{}]:\t{}\n".format(now, m.as_string))
                else:
                    init(ctx, **kwargs)

                if post_setup is not None:
                    post_setup(ctx, **kwargs)

                ctx.sys.Listener.start()

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
