.. |mongo shell| replace:: Mongo shell
.. _page_troubleshooting:

Troubleshooting
===============

Tensorflow Issues
*****************

:tensorflow.python.framework.errors_impl.UnknownError:

  If you are using an RTX graphics card this is more than likeley due to your tesnorflow not supporting them. Simply either use the CPU, another graphics card, or re-compile tensorflow on your system so that it has RTX support.


.. _section_ts_mongodb:

MongoDB/ Serving Issues
***********************

:Error\: not master and slaveOk=false:

  This error means you have attempted to read from a replica set that is not the master. If you would like to read from SECONDARY-ies/ slaves (anything thats not the PRIMARY) you can:

  :|mongo shell|\::

    .. parsed-literal::

        `rs.slaveOk() <https://docs.mongodb.com/manual/reference/method/rs.slaveOk/>`_

:pymongo.errors.OperationFailure\: Authentication failed:

  This error means likely means that your authentication credentials are incorrect, you will want to check the values you are passing to pymongo via Nemesyst to ensure they are what you are expecting. In particular pay special attention to Mongo().connect() as it is the life blood of all connections but since the driver is a lazy driver it wont fail until you attempt to use the connection.
