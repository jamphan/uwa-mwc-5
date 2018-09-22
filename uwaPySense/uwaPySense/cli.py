""" This routine is to handle all the command line options. It is separated
from the main rountine for tidyness. It will be responsible for capturing
all user flags as well as data validation.
"""

import argparse

import uwaPySense.messages

VALID_MSG_TYPES = {'RF': uwaPySense.messages.RFMsg}

def arg_parser():

    parser = argparse.ArgumentParser(description='UWA PySense')

    # Specify the serial port
    parser.add_argument('-p',
                        action='store',
                        default=None,
                        dest='serial_port',
                        help='Specify the serial port the listener is connected to')

    # Specify the output file
    parser.add_argument('-o',
                        action='store',
                        default=None,
                        dest='output_file',
                        help='Specify the output file to write data to')

    # Specify the baud rate of the serial port
    parser.add_argument('--baud-rate',
                        type=float,
                        action='store',
                        default='9600',
                        dest='baud_rate',
                        help='Specify the serial port baud rate')

    # Specify the time out for the serial port
    parser.add_argument('--time-out',
                        type=float,
                        action='store',
                        default='10',
                        dest='time_out',
                        help='Specify a readline time-out for the serial port')

    # Specify the message structure
    parser.add_argument('--message-type',
                        action='store',
                        default='Test',
                        dest='message_type',
                        help='Specify the message structure')

    # Get the arguments
    args = parser.parse_args()

    # Data validation
    stop_flag = False
    err_list = []

    if args.serial_port is None:
        stop_flag = True
        err_list.append("Must specify a serial port with -p")

    if args.message_type not in VALID_MSG_TYPES:
        stop_flag = True
        err_list.append("Message type must be one of: {}".format(",".join(VALID_MSG_TYPES)))
    else:
        args.message_type = VALID_MSG_TYPES[args.message_type]

    if args.time_out <= 0:
        stop_flag = True
        err_list.append("Time out must be real and greater than zero")

    # We want to capture all input errors at once and report it to user
    # this prevents users from having to 'fix-test-fix-test'-ing
    if stop_flag:
        err_msg = 'Errors detected with arguments.\n\n'
        err_msg += '\n'.join(err_list)
        raise Exception(err_msg)
        return None
    else:
        return args