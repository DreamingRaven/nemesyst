.. |mongo shell| replace:: Mongo shell
.. _page_troubleshooting:

Troubleshooting
===============

.. _section_ts_mongodb:

MongoDB/ Serving Issues
+++++++++++++++++++++++

:Error\: not master and slaveOk=false\::

  This error means you have attempted to read from a replica set that is not the master. If you would like to read from SECONDARY-ies/ slaves (anything thats not the PRIMARY) you can:

  :|mongo shell|\::

    .. parsed-literal::

        `rs.slaveOk() <https://docs.mongodb.com/manual/reference/method/rs.slaveOk/>`_
