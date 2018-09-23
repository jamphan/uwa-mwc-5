Quickstart
==========

Setup
-----

To install, you need to navigate to the package directory. The package directory
is such that when you list-directory with ``ls`` you can see a ``setup.py`` file

.. code-block:: bash

    $ python -m pip install -e .

Because the package is currently under a proof-of-concept stage, and that it is
not published (yet) we recommend installing with the ``-e`` switch.

The most basic example
----------------------

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

