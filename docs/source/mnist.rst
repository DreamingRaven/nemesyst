.. _mnist: http://yann.lecun.com/exdb/mnist/
.. |mnist| replace:: MNIST

.. _sklearn: https://scikit-learn.org/stable/index.html
.. |sklearn| replace:: scikit-learn

.. _mongodb compass: https://www.mongodb.com/products/compass
.. |mongodb compass| replace:: MongoDB Compass

.. _mongo shell: https://docs.mongodb.com/manual/mongo/
.. |mongo shell| replace:: Mongo shell

.. _mongodb: https://www.mongodb.com/
.. |mongodb| replace:: MongoDB

.. _gridfs: https://docs.mongodb.com/manual/core/gridfs/
.. |gridfs| replace:: gridfs

.. _keras: https://keras.io/
.. |keras| replace:: Keras

.. |files-only| replace:: :ref:`section_files-only`

Full |mnist|_ Example
=====================

|mnist|_ is a popular well known dataset for evaluating machine learning models. It has been effectively solved at this point, but it is still a good starting point for getting to know how Nemesyst works, and to be able to show people how to use Nemesyst in practice.
It is also relatively clean so there is little pre-processing that is required other than turning it into a directly usable form.

The dataset will be downloaded for you by the cleaning module.

Requirements
++++++++++++

Please ensure you have both |mongodb|_ and the following installed as a bare minimum:

:``examples/requirements/mnist.txt``:

  .. literalinclude:: ../../examples/requirements/mnist.txt

If you are using pip you can quickly install these using:

:|files-only| pip requirements installation example\::

  .. parsed-literal::

    pip install -r examples/requirements/mnist.txt

.. note::

    Please also ensure you have the Nemesyst files at hand ( |files-only| ) as they have all the extra files you will need later on, which are only present in |files-only|

.. _section_mnist_config:

Configuring
+++++++++++

For this example we have created a configuration file for you so there is nothing additional that needs to be done. It is advised that you read it through. It is a `.ini` style file. However each of these options can be passed in to Nemesyst as cli or environment options as well but we believed it would be a much nicer introduction to have them in a configuration file.

:``examples/configs/nemesyst/mnist.conf``:

  .. literalinclude:: ../../examples/configs/nemesyst/mnist.conf

If you would like to skip rest of this example for whatever reason such as you are more interested in checking Nemesyst is working simply remove the symbol "`;`" from the start of any lines it appears in to uncomment that line, and then run everything using:

:|files-only| automated example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf


Serving
+++++++

For this example Nemesyst will create a database for us whenever we call the config file since we pass in options to initialise and start the database (see :ref:`section_mnist_config`). We can do this using:

:|files-only| serving example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --db-init --db-start

This example will start the database, to close the database you can:

:|files-only| stopping database example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --db-stop

.. note::

  Nemesyst may ask you a password. As long as you are using the same password between runs it wont cause you issue as you are simultaneously using and creating (when using --db-init) the password for the default user in our config file, you can change this behavior but we wanted to include it so we don't end up creating universal passwords that lazy users might oversee.

  For more complex scenarios pleas refer to :ref:`page_serving`

Checking up on the database
+++++++++++++++++++++++++++

It may be necessary after each of the following steps to check on the database to ensure it has done exactly what you expect it to be doing. To login to the database easily you can use:

:|files-only| logging into running database example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --db-login

This should put you in the |mongo shell|_ which is a javascript based interface of |mongodb|_ for direct user intervention. Where you can do all sorts of operations and checks. This is of course optional but recommended. If you would rather a more graphical interface you can use any of the plethora of tools to visualise the database but we recommend |mongodb compass|_, in particular for its aggregation helper.

Cleaning
++++++++

In this step we will launch the example |mnist|_ cleaner which downloads the data using |sklearn|_ to get a much cleaner version of the data set for us. Then inserting the data into individual dictionaries row wise, so that each dictionary is a single complete example/ observation, with associated target feature. To put it back into the database we need only yield each dictionary and Nemesyst will handle iteration for us. This document dictionary can also be used to house useful metadata about the dataset so that you can further filter using more advanced Nemesyst and MongoDB functionality that go beyond the scope of this simple introduction.

To begin cleaning you need only tell Nemesyst to clean the data using:

:|files-only| cleaning example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --data-clean

The example |mnist|_ cleaner is shown below for convenience.

:``examples/cleaners/mnist_cleaner.py``:

  .. literalinclude:: ../../examples/cleaners/mnist_cleaner.py

Learning
++++++++

To learn from the now cleaned database-residing data, you can:

:|files-only| learning example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --dl-learn

This example trains a CNN, and yields a tuple ``(metadata_dictionary, pickle.dumps(model))`` which is then stored in |mongodb|_ using |gridfs| as most models exceed the base |mongodb|_ 16MB document size limit.
This example is derived from one of the pre-existing |keras|_ |mnist|_ examples, but transformed into a relatively efficient Nemesyst variant.
The major differences are that we use `fit_generator` which takes a generator (in our case a database cursor and pre-processor) for the training set, and another generator for the validation set. For this example we have simply validated against the test set as we aren't attempting to blind ourselves for the purposes of scientific rigor and overfitting prevention.
Care should be taken in reading the pipelines as they can be quite complex operations to solve very tough problems, but here we simply set them to separate the dataset into train, and validation.

:``examples/learners/mnist_learner.py``:

  .. literalinclude:: ../../examples/learners/mnist_learner.py

Inferring
+++++++++

.. warning::

  Work in progress section

In this stage we retrieve the model trained previously stored in |mongodb|_ as |gridfs|_ chunks and unpack the model again for reuse and prediction.
We can predict using the |gridfs|_ stored model by passing:

:|files-only| inferring example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --i-predict
