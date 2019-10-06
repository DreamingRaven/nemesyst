.. _mnist: http://yann.lecun.com/exdb/mnist/
.. |mnist| replace:: MNIST

.. _sklearn: https://scikit-learn.org/stable/index.html
.. |sklearn| replace:: scikit-learn

.. |files-only| replace:: :ref:`section_files-only`

Full |mnist|_ Example
=====================

|mnist|_ is a popular well known dataset for evaluating machine learning models. It has been effectively solved at this point, but it is still a good starting point for getting to know how Nemesyst works, and to be able to show people how to use Nemesyst in practice.
It is also relatively clean so there is little pre-processing that is required other than turning it into a directly usable form.

The dataset will be downloaded for you by the cleaning module.

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

  For more complex scenarios pleas refer to :ref:`page_serving`

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

placeholder

Inferring
+++++++++

placeholder
