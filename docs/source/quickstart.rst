Quickstart
==========

The UWAste solution is a SmartBin WSN solution over many
different systems. Thus, this repository is a multi-package repository. 
You will need to navigate to the individual components, depending on what system
you wish to develop.

.. note::

   Throughout the documentation, we will refer to the **TLD**, this is in reference to the repo folder.
   That is, when you are located in the **TLD** and run ``ls``, you should see the ``LICENSE``, ``README.md``,
   and ``.gitignore`` files (among other files).

+---------------------------------+----------------------------------------------------------------------------+
|            Component            |                                Description                                 |
+=================================+============================================================================+
| :ref:`listener-overview`        | Bridges a WSN to the TCP/IP network and publishes the information via MQTT |
+---------------------------------+----------------------------------------------------------------------------+
| :ref:`server-database-overview` | Stores all data from the WSN, allowing for data visualiation               |
+---------------------------------+----------------------------------------------------------------------------+
| :ref:`web-application-overview` | The python Flask/MQTT application that displays the dashboard              |
+---------------------------------+----------------------------------------------------------------------------+
| :ref:`mote-overview`            | The mote sensing devices deployed in the WSN                               |
+---------------------------------+----------------------------------------------------------------------------+