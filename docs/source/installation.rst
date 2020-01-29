.. _page_installation:

.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. |git| replace:: git

.. _python:  https://www.python.org/
.. |python| replace:: python

.. _mongodb: https://www.mongodb.com/
.. |mongodb| replace:: MongoDB

.. _docker: https://www.docker.com/
.. |docker| replace:: Docker

.. _bash shell: https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29
.. |bash shell| replace:: Bash shell

Installation
============

.. note::

    Certain distributions link ``python`` to ``python2`` and others link it to ``python3``.
    For disambiguation python, pip, and virtualenv shall mean their python v3 versions here, i.e. ``python3``, ``pip3``, ``virtualenv3``.

.. warning::

    You will need to have |git|_, and |python|_ installed any of the below methods to work.
    You will also need |mongodb|_ if you intend to create a local database, (more than likely), but Nemesyst will still connect to already running databases without it if you happen to have one already.

This section will outline various methods for installation of Nemesyst, and its dependencies. Not all methods are equal there are slight variations between them, which are outlined in the respective sections below, along with instructions for each method:

.. contents:: :local:

.. _section_files-only:

Files-only/ development
***********************

.. |minimal_requirements| replace:: ``./nemesyst/requirements.txt``

.. |maximal_requirements| replace:: ``./nemesyst/docs/requirements.txt``

This method of files-only installation provides the user with all the additional utility files, and examples needed during development. This includes the files necessary for the :ref:`page_mnist`, and is advised when first starting to use Nemesyst so that you can better understand what is going on. In production however you do not need all these additional files so other slimmer/ more streamlined methods of installation are better.

    Pros:

    - All the example files for quickly getting to grips with Nemesyst.
    - Easy to understand as the files are not filed away somewhere obscure.
    - Easy to install example dependencies as you can ``pip install -r requirements.txt`` or whatever other requirements list we include.
    - Unit tests available.

    Cons:

    - You are responsible for ensuring the requirements are met for Nemesyst, such as |python|_, |git|_, and |mongodb|_.
    - It is less repeatable/ deployable as most steps are manual as opposed to the other available methods of installation.

Getting the files
+++++++++++++++++

To retrieve the Nemesyst files you will need |git|_ installed. To download the Nemesyst directory in your current working directory you can run:

.. code-block:: bash

    git clone https://github.com/DreamingRaven/nemesyst

Installing dependancies
+++++++++++++++++++++++

To make use of Nemesyst directly now that you have the files you need to have installed:

System dependencies:

    1. |python|_ (required): Nemesyst is written in |python|_, you wont get far without it.
    2. |git|_ (required): To install, and manage Nemesyst files.
    3. |mongodb|_ (recommended): If you want to be able to create, and destroy a local |mongodb|_ database.
    4. |docker|_ (optional): If you want to manage local containerized |mongodb|_ databases.

Python dependencies:

    :|minimal_requirements|:

        .. literalinclude:: ../../requirements.txt

        You can install these quickly using:

        :|bash shell|_ installing dependancies from file:

            .. parsed-literal::

                pip install -r ``./nemesyst/requirements.txt``

        or:

        :|bash shell|_ installing Nemesyst and dependancies using setup.py:

            .. parsed-literal::

                python setup.py install

    Optionally if you would like to build the Nemesyst documentation, and/ or use the full testing suite you will require |maximal_requirements|:

    .. literalinclude:: ../requirements.txt


.. _section_automated:

Automated
*********

This section discusses the more automated and repeatable installation methods for Nemesyst, but they do not contain all the files needed to learn, and begin developing Nemesyst integrated applications, rather this includes just the bare-bones Nemesyst ready for your deployment.

Generic
+++++++

For now you can use pip via:

.. code-block:: bash

  pip install git+https://github.com/DreamingRaven/nemesyst.git#branch=master

Archlinux
+++++++++

Install `nemesyst-git <https://aur.archlinux.org/packages/nemesyst-git/>`_:sup:`AUR`.

Manual
******

Generic
+++++++

.. code-block:: bash

  git clone https://github.com/DreamingRaven/nemesyst
  cd nemesyst
  python setup.py install

Archlinux
+++++++++

.. code-block:: bash

  git clone https://github.com/DreamingRaven/nemesyst
  cd nemesyst/.arch/
  makepkg -si

.. _section_virtual-env:

Virtual env
***********

To create the `python-virtualenv <https://wiki.archlinux.org/index.php/Python/Virtual_environment>`_:

.. code-block:: bash

    vituralenv venv

To then use the newly created virtual environment:

.. code-block:: bash

    source venv/bin/activate

OR if you are using a terminal like fish:

.. code-block:: bash

    source venv/bin/activate.fish

To install Nemesyst and all its dependencies into a virtual environment while it is being used (activated):

.. code-block:: bash

    pip install git+https://github.com/DreamingRaven/nemesyst.git#branch=master

To exit the virtual environment:

.. code-block:: bash

      deactivate
