.. _mnist: http://yann.lecun.com/exdb/mnist/
.. |mnist| replace:: MNIST
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

In this step we wil

:|files-only| cleaning example\::

  .. parsed-literal::

    ./nemesyst --config ./examples/configs/nemesyst/mnist.conf --data-clean

Learning
++++++++

test

Inferring
+++++++++

test
