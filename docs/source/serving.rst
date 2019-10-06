.. |files-only| replace:: :ref:`section_files-only`

.. _sklearn: https://scikit-learn.org/stable/index.html
.. |sklearn| replace:: scikit-learn

.. _mongodb: https://www.mongodb.com/
.. |mongodb| replace:: MongoDB

.. _yaml: https://yaml.org/
.. |yaml| replace:: yaml

.. |mongo shell| replace:: Mongo shell
.. |bash shell| replace:: Bash shell

.. _docker: https://www.docker.com/
.. |docker| replace:: Docker


.. _docker-compose: https://docs.docker.com/compose/
.. |docker-compose| replace:: Docker-Compose

.. |troubleshooting| replace:: :ref:`section_ts_mongodb`
.. _page_serving:

Serving
=======

Nemesyst uses |mongodb|_ as its primary message passing interface. This page will more elaborate on using Nemesyst with different database setups, debugging, common issues, and any nitty-gritty details that may be necessary to discuss.

.. warning::
  While Nemesyst does support using mongodb.yaml files for complex db setup, care should be taken that Nemesyst is not overriding the values you were expecting in the config files. Things such as the DBs path are almost always overridden along with the port to use by default even if the user has not provided that argument. In future we intend to make it such that hard coded defaults when not overridden by the user, first attempt to look in the mongodb.yaml file before falling back to hard-coded values.

Creating a basic database
+++++++++++++++++++++++++

Disambiguation: we define a basic database as a standalone |mongodb|_ instance with one universal administrator and one read/write user with password authentication.

While it is possible it is highly discouraged to use Nemesyst to create the users you require as this is quite complicated to manage and may lead to more problems than its worth compared to simply creating a database and adding a user manually using something like the following:

.. _manual_mongodb:

Manual creation of |mongodb|_
-----------------------------

:|files-only| creation of database example\::

  .. parsed-literal::

      mongod --config ./examples/configs/basic_mongo_config.yaml

This will create a database with all the |mongodb|_ defaults as it is an empty |yaml|_ file.
If you would instead want a more complex setup please take a look at ``examples/configs/authenticated_replicaset.yaml`` instead, but you will need to generate certificates and keys for this so it is probably a poor place to start but will be what you will want to use in production as a bare minimum security.

|docker-compose|_ creation of |mongodb|_
----------------------------------------

:|docker-compose|_, |files-only| creation of database example\::

  .. parsed-literal::

      docker-compose up

This similar to the :ref:`manual_mongodb` creation uses a simple config file to launch the database. This can be changed in ``docker-compose.yaml``.
At this point you will need to connect to the running |mongodb|_ instance (see: :ref:`connecting_mongodb`) to create your main administrator user, with "userAdminAnyDatabase" role.
After this you can use the following to close the |docker|_ container with the database:

:|docker-compose|_, |files-only|, closing |docker-compose|_ database example\::

  .. parsed-literal::

      docker-compose down

.. note::
  Don't worry we set our docker-compose.yaml to save its files in ``/data/db`` so they are persistent between runs of docker-compose. If you need to delete the |mongodb|_ database that is where you can find them.

.. _connecting_mongodb:

Connecting to a running database
--------------------------------

To be able to fine tune, create users, update etc it will be necessary to connect to |mongodb|_ in one form or another. Nemesyst can help you log in or you can do it manually.

 .. note::
   If there is no `userAdmin or userAdminAnyDatabase <https://docs.mongodb.com/manual/reference/built-in-roles/#userAdmin>`_ then unless expressly configured there will be a localhost exception which will allow you to log in and create this user. If this user exists the localhost exception will close. Please ensure you configure this user as they can grant any role or rights to anyone and would be a major security concern along with making it very difficult to admin your database.

Nemesyst
********

:todo:

  Include instructions for logging into |mongodb|_ from Nemesyst.
  Still needs addition

Mongo
*****

To connect to an non-sharded database with autnentication but no TLS/SSL:

:|bash shell| example\::

  .. parsed-literal::

      mongo HOSTNAME:PORT -u USERNAME --authenticationDatabase DATABASENAME

To connect to a slightly more complicated scenario with authentication, TLS, and sharding enabled:

:|bash shell| example\::

  .. parsed-literal::

      mongo HOSTNAME:PORT -u USERNAME --authenticationDatabase DATABASENAME --tls --tlsCAFile PATHTOCAFILE --tlsCertificateKeyFile PATHTOCERTKEYFILE

Creating database users
-----------------------

You will absolutely need a user with at least "userAdminAnyDatabase" role.
Connect to the running database see :ref:`connecting_mongodb`.

:|mongo shell| create a new role-less user\::

  .. parsed-literal::

    db.createUser({user: "USERNAME", pwd: passwordPrompt(), roles: []})

:|mongo shell| grant role to existing user example\::

  .. parsed-literal::

    db.grantRolesToUser(
    "USERNAME",
    [
      { role: "userAdminAnyDatabase", db: "admin" }
    ])

:|mongo shell| create user and grant userAdminAnyDatabase in one\::

  .. parsed-literal::

    db.createUser({user: "USERNAME", pwd: passwordPrompt(), roles: [{role:"userAdminAnyDatabase", db: "admin"}]})

.. note::
  Since this user belongs to admin in the previous examples that means the authenticationDatabase is admin when authenticating as this user as per the instructions in ":ref:`connecting_mongodb`".

From basic database to replica sets
+++++++++++++++++++++++++++++++++++

:todo:

  Include instructions for turning a database into several replica sets.

Troubleshooting
+++++++++++++++

Please see |troubleshooting|

Further reading
+++++++++++++++

`MongoDB config file options <https://docs.mongodb.com/manual/reference/configuration-options/>`_
