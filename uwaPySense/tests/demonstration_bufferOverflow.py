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

With the parameters set, we can see that the serial buffer grows over time.
Eventually, the script will stop writing to STDOUT indiciating that the buffer
is full. In this simulation environment, the SerialSimulator thread simply
waits until there is space in the buffer and writes (hence a reduced STDOUT
throughput). But in practice, the sensor will have an input buffer overflow
likely skipping input data.

NOTE: Use Ctrl+C (Break) to stop the program
"""

import sys
import time
import threading

from tests.test_serial import SerialTestClass

# ------------------------------------------------------------------------------
# PARAMETERS
SAMPLING_FREQ = 100 # samples/sec

# Delays
DELAY_WRITE = 0.01 # seconds
DELAY_NETWORK = 0.01 # seconds
# ------------------------------------------------------------------------------

def SerialSimulator(port, event):

    counter = 0

    while not(event.is_set()):
        time.sleep(1/SAMPLING_FREQ)
        port.write('{}\n'.format(counter))
        print('{},{}\n'.format(counter, port.in_waiting))
        counter += 1

def main():

    s = SerialTestClass()

    e = threading.Event()
    e.clear()

    thr = threading.Thread(target=SerialSimulator, args=(s,e,))
    thr.start()

    try:
        while not(e.is_set()):
            ser_bytes = s.readline()
            time.sleep(DELAY_NETWORK + DELAY_WRITE)
            print(ser_bytes)
    except KeyboardInterrupt:
        e.set()

if __name__ == '__main__':
    main()