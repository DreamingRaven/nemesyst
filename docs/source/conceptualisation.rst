.. _section_conceptualisation:

Conceptualisation
=================

.. _section_nemesyst-literal:

Nemesyst Literal un-abstract stages
***********************************

.. figure:: nemesyst_example.svg
    :alt: Nemesyst use-case example diagram.
    :figclass: align-center

    This image is a use case example of Nemesyst applied to a distributed refrigeration fleet over multiple sites, and both online and offline learning capabilities occuring simultaneously.

.. _section_nemesyst-abstraction:

Nemesyst Abstraction of stages
******************************

.. figure:: nemesyst_stages.svg
    :alt: Nemesyst stages of data from input to output.
    :figclass: align-center

    Deep learning can be said to include 3 stages, data-wrangling, test-training, and infering. Nemesyst adds an extra layer we call serving, which is the stage at which databases are involved as the message passing interface (MPI), and generator, between the layers, machines, and algorithms, along with being the data, and model storage mechanism.

.. _section_wrangling:

Wrangling
*********

.. figure:: nemesyst_wrangling.svg
    :alt: Nemesyst wrangling puzzle diagram.
    :figclass: align-center

    Wrangling is the stage where the data is cleaned into single atomic examples to be imported to the database.
    See :ref:`section_all-options` for a full list of options.

.. _section_serving:

Serving
*******

.. figure:: nemesyst_serving.svg
    :alt: Nemesyst database serving puzzle diagram.
    :figclass: align-center

    Serving is the stage where the data and eventually trained models will be stored and passed to other processess potentially on other machines.
    See :ref:`section_all-options` for a full list of options.

.. _section_learning:

Learning
********

.. figure:: nemesyst_learning.svg
    :alt: Nemesyst learning puzzle diagram.
    :figclass: align-center

    Learning is the stage where the data is used to train new models or to update an existing model already in the database.
    See :ref:`section_all-options` for a full list of options.

.. _section_infering:

Infering
********

.. figure:: nemesyst_infering.svg
    :alt: Nemesyst inference puzzle diagram.
    :figclass: align-center

    Infering is the stage where the model(s) are used to predict on newly provided data.
    See :ref:`section_all-options` for a full list of options.
