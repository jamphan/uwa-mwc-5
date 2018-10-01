.. _listener-overview:

Listener
========

``Listners`` bridge wireless sensor networks to TCP/IP networks.
They are responsible for collecting all messages from the motes and publishing them
with the MQTT protocol.

The ``Listener`` connects to a mote through serial.

Quickstart
----------

Navigate to the TLD. You will need to install the ``uwaPySense`` package using pip

.. code-block:: bash

   $ cd /path/to/Repo/                      # TLD
   $ python -m pip install -r ./uwaPySense/requirements.txt
   $ python -m pip install -e ./uwaPySense/

Because the package is currently under a proof-of-concept stage, and that it is
not published (yet) we recommend installing with the ``-e`` switch.

Using the default configurations, the script below is all that is required:

.. note::
   
   The default ``Listener`` configuration listens for all messages on the serial
   line the are not blank and end with a newline.


.. code-block:: bash

   $ python -m uwaPySense -p <PORT>

Configuration
-------------

The package offers several configurations to suit your network implementaiton.
To do so, you must specify your own custom script that enumerate these configurations.
For example:

.. code-block:: python

    # my_listener.py

    from datetime import datetime
    import uwaPySense

    app = uwaPySense.App()

    @uwaPySense.messages.end_flag
    def flag(m):

        return 'END'

    @uwaPySense.messages.is_valid
    def valid(m):

        if len(m.as_string) > 0 and m.as_string[0].isdigit():
            return True
        else:
            return False

    @app.addwork
    def _(m):
        print("[{}]:\t{}".format(datetime.now(), m.as_string))        

    @app.addwork
    def _(m):
    
        with open('output.txt', 'a') as fd:
            fd.write("[{}]:\t{}".format(datetime.now(), m.as_string))      
    
    @app.setup()
    def config(ctx):
        print("\nListening on {}".format(ctx.serial_port))
        print("\tBaud rate = {:.0f}".format(ctx.baud_rate))
        print("\tTime out = {:.2f}".format(ctx.time_out))
        print("Press Ctrl+C to stop\n")

        ctx.counter = 0

    @app.loop(rest_time=60)
    def main(ctx):
        """ Program main loop"""

        ctx.counter += 1
        print("Time elapsed = {} mins".format(ctx.counter))

    if __name__ == '__main__':
        main()

You can then call this script, and the program will run as configured. In this
example, the following configurations were made

- The ``flag()`` decorated function specifies the end of the frame for all messages. In this case the string sequence ``END``
- the ``valid()`` decorated function specifies the conditions that a message is considered valid
- the ``confg()`` decorated function specifies any setup required before the main loop begins
- the ``@addwork`` decorators specify additional work the ``Worker`` should perform for every message
- the ``main()`` decorated function modifies the ``Listener`` loop to keep a counter that was setup in the ``config()`` routine

Note, that you **must** specify a port for the Listener to listen to with the ``-p`` flag.

Once the ``my_listener.py/`` script is saved, you simply run the program from console as follows

.. code-block:: bash

   $ python my_listener.py -p COM3

Notice how all the command line switches are carried over to your script.

You can also specify the baud-rate with the ``--baud-rate`` flag

.. code-block:: bash

   $ python my_listener.py -p COM3 --baud-rate 9600

For more information see:

.. code-block:: bash

   $ python my_listener.py --help

Design
------

The Listener is a multi-thread process, which recieves data from its host's 
serial line, and writes data - either to file, or through a TCP/IP network.

The two core types of threads that the Listener process runs is its main
thread (``Listener``) and a ``Worker`` thread. The ``Listener`` instance handles
all incoming data on the serial line; it's core functions are to:

- Clear the serial recieve buffer to prevent the less powerful serial device from overflowing its transmit serial buffer
- Identify if the inbound messages are valid, and if they are
- Put the valid messages into a queue for processing

The ``Worker`` thread reads from the queue and is responsible for;

- Formatting messages into writable forms
- Writing the messages into storage

Inspecting the ``__main__.py`` package module, we can see that three core objects
must be instantiated:

- The ``Listener`` class
- The ``Worker`` class
- The ``Serial`` class

.. code-block:: python

    def main():
        """ Program entry point."""

        args = uwaPySense.cli.arg_parser()

        s = serial.serial_for_url(url=args.serial_port,
                                timeout=args.time_out,
                                baudrate=int(args.baud_rate))

        l = Listener(s, message_prototype=args.message_type)
        l.set_worker(Worker())
        l.start()

        loop()

The ``Worker`` object is assigned to the ``Listener`` through the ``set_worker()``
method. This was done to allow developers to have full contorl on how they
wish to setup their own custom workers.

.. note::

   A ``Worker`` class of class ``uwaPySense.Server.StoppableThread`` must be set to the
   ``Listener`` before the main loop can be run