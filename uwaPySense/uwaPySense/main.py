import time
import serial
import argparse

from uwaPySense.Server import Listener
import uwaPySense.messages


VALID_MSG_TYPES = {"Test": uwaPySense.messages.Msg, 'RF': uwaPySense.messages.RfMsg}

def main():
    """ Program entry point."""

    args = cli_parser()

    if args.debug_mode:   
        loop_debug(args)
    else:
        loop(args)

    return 0

def cli_parser():
    """ This routine is to handle all the command line options. It is separated
    from the main rountine for tidyness. It will be responsible for capturing
    all user flags as well as data validation.
    """
    parser = argparse.ArgumentParser(description='UWA PySense')

    # Debug mode will only use a fake serial port
    parser.add_argument('--debug',
                        action='store_true',
                        default=False,
                        dest='debug_mode',
                        help='Set to DEBUG mode which will use a test serial port')

    # Specify the serial port
    parser.add_argument('-p',
                        action='store',
                        default=None,
                        dest='serial_port',
                        help='Specify the serial port the listener is connected to')

    parser.add_argument('--baud-rate',
                        action='store',
                        default='9600',
                        dest='baud_rate',
                        help='Specify the serial port baud rate')

    parser.add_argument('--time-out',
                        action='store',
                        default='0',
                        dest='time_out',
                        help='Specify the serial port time-out')

    parser.add_argument('--message-type',
                        action='store',
                        default='Test',
                        dest='message_type',
                        help='Specify the message structure')

    args = parser.parse_args()

    # Data validation
    stop_flag = False
    err_list = []

    if not(args.debug_mode):
        
        if args.serial_port is None:
            stop_flag = True
            err_list.append("Must specify a serial port with -p")

        if not(args.baud_rate.isdigit()):
            stop_flag = True
            err_list.append("The baud rate must be an integer")

        if args.message_type not in VALID_MSG_TYPES:
            stop_flag = True
            err_list.append("Message type must be one of: {}".format(",".join(VALID_MSG_TYPES)))

    if stop_flag:
        err_msg = 'Errors detected with arguments.\n\n'
        err_msg += '\n'.join(err_list)
        raise Exception(err_msg)
        return None
    else:
        return args

def loop_debug(args):

    from tests.test_serial import SerialTestClass
    s = SerialTestClass()
    l = Listener(s, message_prototype=VALID_MSG_TYPES[args.message_type])
    l.start()

    try:
        while(True):
            time.sleep(0.05)
            s.write('msg:test' + '\n')
    except KeyboardInterrupt:
        l.stop()

def loop(args):

    s = serial.serial_for_url(url=args.serial_port,
                              timeout=float(args.time_out),
                              baudrate=int(args.baud_rate))

    l = Listener(s, message_prototype=VALID_MSG_TYPES[args.message_type])
    l.start()

    print('Listening...')
    print('Ctrl+C to stop\n')

    mins_elapsed = 0
    try:
        while(True):
            time.sleep(60) # A delay is required so that the user can break program
            mins_elapsed += 1
            print("\tTime elapsed: {} mins".format(mins_elapsed))
    except KeyboardInterrupt:
        l.stop()

if __name__ == '__main__':
    main()