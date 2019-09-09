.. |mongo shell| replace:: Mongo shell
.. |bash shell| replace:: Bash shell
.. |troubleshooting| replace:: :ref:`section_ts_mongodb`
.. _page_serving:

Serving
=======

Nemesyst uses MongoDB as its primary message passing interface. This page will more elaborate on using Nemesyst with different database setups, debugging, common issues, and any nitty-gritty details that may be necessary to discuss.

.. warning::
  While Nemesyst does support using mongodb.yaml files for complex db setup, care should be taken that Nemesyst is not overriding the values you were expecting in the config files. Things such as the DBs path are almost always overridden along with the port to use by default even if the user has not provided that argument. In future we intend to make it such that hard coded defaults when not overridden by the user, first attempt to look in the mongodb.yaml file before falling back to hard-coded values.

Creating a basic database
+++++++++++++++++++++++++

disambiguation: we define a basic database as a standalone MongoDB instance with one universal administrator and one read/write user with password authentication.

While it is possible it is highly discouraged to use Nemesyst to create the users you require as this is quite complicated to manage and may lead to more problems than its worth compared to simply using something such as:

:todo:

  Include example for basic database creation

Connecting to a running database
++++++++++++++++++++++++++++++++

To be able to fine tune, create users, update etc it will be necessary to connect to MongoDB in one form or another. Nemesyst can help you log in or you can do it manually.

 .. note::
   If there is no `userAdmin or userAdminAnyDatabase <https://docs.mongodb.com/manual/reference/built-in-roles/#userAdmin>`_ then unless expressly configured there will be a localhost exception which will allow you to log in and create this user. If this user exists the localhost exception will close. Please ensure you configure this user as they can grant any role or rights to anyone and would be a major security concern along with making it very difficult to admin your database.

Nemesyst
--------

:todo:

  Include instructions for logging into mongodb from Nemesyst.

Mongo
-----

To connect to an non-sharded database with autnentication but no TLS/SSL:

:|bash shell| example\::

  .. parsed-literal::

      mongo HOSTNAME:PORT -u USERNAME --authenticationDatabase DATABASENAME

To connect to a slightly more complicated scenario with authentication, TLS, and sharding enabled:

:|bash shell| example\::

  .. parsed-literal::

      mongo HOSTNAME:PORT -u USERNAME --authenticationDatabase DATABASENAME --tls --tlsCAFile PATHTOCAFILE --tlsCertificateKeyFile PATHTOCERTKEYFILE

From basic database to replica sets
+++++++++++++++++++++++++++++++++++

:todo:

  Include instructions for turning a database into several replica sets.

Troubleshooting
---------------

Please see |troubleshooting|
