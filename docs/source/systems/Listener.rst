Listner
=======

The ``Listner`` class is responsible for collecting all messages and writing 
them into storage.

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