import time
import serial

from uwaPySense.Server import Listener, Worker, loop
import uwaPySense.cli
import uwaPySense.messages

def main():
    """ Program entry point."""

    args = uwaPySense.cli.arg_parser()

    s = serial.serial_for_url(url=args.serial_port,
                              timeout=args.time_out,
                              baudrate=int(args.baud_rate))

    l = Listener(s, message_prototype=args.message_type)
    l.set_worker(Worker())
    l.start()

    print('Listening...')
    print('Ctrl+C to stop\n')

    loop()

if __name__ == '__main__':
    main()