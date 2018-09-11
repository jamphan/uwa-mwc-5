from uwaPySense.Server import Listener
import time

def main():

    TEST = True

    if TEST:
        from tests.test_serial import SerialTestClass
        s = SerialTestClass()

    l = Listener(s)
    l.start()

    try:
        while(True):
            if TEST:
                time.sleep(0.01)
                s.write('msg:test' + '\n')

    except KeyboardInterrupt:
        l.stop()

if __name__ == '__main__':
    main()