.. |files-only| replace:: :ref:`section_files-only`

.. _section_overview:

Overview
========

.. _section_nemesyst-literal:

Nemesyst literal un-abstract stages
***********************************

.. figure:: nemesyst_example.svg
    :alt: Nemesyst use-case example diagram.
    :figclass: align-center

    This image is a use case example of Nemesyst applied to a distributed refrigeration fleet over multiple sites, and both online and offline learning capabilities occuring simultaneously.

Nemesyst has been made to be generic enough to handle many possible configurations, but we cannot possibly handle all possible scenarios. Sometimes it may be neccessary to manually configure certain aspects of the process, especially regarding MongoDB as it is quite a well developed, mature, database, with more features than we could, and should automate.

.. _section_nemesyst-abstraction:

Nemesyst Abstraction of stages
******************************

.. figure:: nemesyst_stages.svg
    :alt: Nemesyst stages of data from input to output.
    :figclass: align-center

    Nemesyst has abstracted, grouped, and formalised what we believe are the core stages of applying deep learning at all scales.

Deep learning can be said to include 3 stages, data-wrangling, test-training, and infering. Nemesyst adds an extra layer we call serving, which is the stage at which databases are involved as the message passing interface (MPI), and generator, between the layers, machines, and algorithms, along with being the data, and model storage mechanism.

.. _section_nemesyst-parallelisation:

Nemesyst Parallelisation
************************

As of: `2.0.1.r6.f9f92c3 <https://github.com/DreamingRaven/nemesyst/commit/f9f92c38c900a0f0bb87e9133aa5b9bb48d60b41>`_

.. figure:: nemesyst_rounds.svg
    :alt: Nemesyst round depiction diagram, showing the order and values of rounds.
    :figclass: align-center

    Nemesyst parallelises each script, up the the maximum number of processes in the process pool.
    See :ref:`section_all-options` for a full list of options.

Local parallelisation of your scripts occur using pythons process pools from multiprocessing. This diagram shows how the rounds of processing are abstracted and the order of them. Rounds do not continue between stages, I.E if there is a spare process but not enough scripts from that stage (e.g cleaning) it will not fill this with a script process from the next stage (e.g learning). This is to prevent the scenario where a learning script may depend on the output of a previous cleaning script.

.. _section_wrangling:

Wrangling
*********

.. figure:: nemesyst_wrangling.svg
    :alt: Nemesyst wrangling puzzle diagram.
    :figclass: align-center

    Wrangling is the stage where the data is cleaned into single atomic examples to be imported to the database.
    See :ref:`section_all-options` for a full list of options.

:|files-only| example:

  .. literalinclude:: ../../tests/cleaning.sh

.. _section_serving:

Serving
*******

.. figure:: nemesyst_serving.svg
    :alt: Nemesyst database serving puzzle diagram.
    :figclass: align-center

    Serving is the stage where the data and eventually trained models will be stored and passed to other processess potentially on other machines.
    See :ref:`section_all-options` for a full list of options.

:|files-only| example:

  .. literalinclude:: ../../tests/serving.sh

.. _section_learning:

Learning
********

.. figure:: nemesyst_learning.svg
    :alt: Nemesyst learning puzzle diagram.
    :figclass: align-center

    Learning is the stage where the data is used to train new models or to update an existing model already in the database.
    See :ref:`section_all-options` for a full list of options.

:|files-only| example:

  .. literalinclude:: ../../tests/learning.sh

.. _section_infering:

Infering
********

As of: `2.0.2.r7.1cf3eab <https://github.com/DreamingRaven/nemesyst/commit/1cf3eab0dd6196c9065f43e9b231a50687f67065>`_

.. figure:: nemesyst_infering.svg
    :alt: Nemesyst inference puzzle diagram.
    :figclass: align-center

    Infering is the stage where the model(s) are used to predict on newly provided data.
    See :ref:`section_all-options` for a full list of options.


:|files-only| example:

  .. literalinclude:: ../../tests/learning.sh
