""" This script is to demonstrate why threading is needed for a scalable WSN.

Changes:
    2018/09/11: Jamie Phan, Initial version

A SerialSimulator is put on a thread to simulate a device on the line pushing
data to the Python client, as shown below:
     ___________                     ___________
    |           |                   |           |
    | Py CLIENT | <---- USB ------- | SENSOR    |
    |___________|                   |___________| 

Note, in the diagram, we can see two blocks indiciating two separate processes;
hence two separate threads for correct simulation.

With the parameters set, we can see that the serial buffer reaches an steady
state value and there is no buffer overflow. 

In order to accomplish this, we have set up a thread on the Client side which
handles writing, whilst the client itself is only responsible for reading the
serial line. The net effect is that the delays have been shifted onto the thread
of the client, whilst the client itself can freely empty the serial buffer.

NOTE: Use Ctrl+C (Break) to stop the program
"""

import threading
import time
import queue

from tests.test_serial import SerialTestClass

# ------------------------------------------------------------------------------
# PARAMETERS
SAMPLING_FREQ = 100 # samples/sec

# Delays
DELAY_WRITE = 0.01 # seconds
DELAY_NETWORK = 0.01 # seconds
# ------------------------------------------------------------------------------

def SerialSimulator(s, event):

    counter = 0

    while not(event.is_set()):
        time.sleep(1/SAMPLING_FREQ)
        s.write('msg:{}\n'.format(counter))
        print('{},{}\n'.format(counter, s.in_waiting))
        counter += 1

def Worker(queue, event):

    while not(event.is_set()): 

        if not(queue.empty()):
            time.sleep(DELAY_NETWORK + DELAY_WRITE)
            print(queue.get_nowait())
            queue.task_done()

def Listener(s, queue, event):

    while not(event.is_set()):

        ser_bytes = s.readline()
        decoded_bytes =  ser_bytes[0:len(ser_bytes)-1].decode("utf-8")

        if decoded_bytes.startswith('msg:'):
            m = decoded_bytes
            queue.put_nowait(m)

def main():

    s = SerialTestClass()

    e = threading.Event()
    e.clear()

    msg_queue = queue.Queue()

    thrSerial = threading.Thread(target=SerialSimulator, args=(s,e,))
    thrWorker = threading.Thread(target=Worker, args=(msg_queue,e,))
    thrListener = threading.Thread(target=Listener, args=(s, msg_queue,e,))

    thrSerial.start()
    thrWorker.start()
    thrListener.start()

    try:
        while(True):
            pass
    except KeyboardInterrupt:
        e.set()

if __name__ == '__main__':
    main()