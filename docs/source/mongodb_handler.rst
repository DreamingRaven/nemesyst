Mongo
=====

Nemesyst MongoDB abstraction/ Handler.
This handler helps abstract some pymongo functionality to make it easier for us to use a MongoDB database for our deep learning purposes.

Example usage
+++++++++++++

Below follows a in code example unit test for all functionality. You can overide the options using a dictionary to the constructor or as keyword arguments to the functions that use them:

.. literalinclude:: ../../nemesyst_core/mongo.py
    :pyobject: _mongo_unit_test

.. warning::

  Mongo uses subprocess.Popen in init, start, and stop, since these threads would otherwise lock up nemesyst, with time.sleep() to wait for the database to startup, and shutdown. Depending on the size of your database it may be necessary to extend the length of time time.sleep() as larger databases will take longer to startup and shutdown.

.. autoclass:: mongo.Mongo
  :members:
