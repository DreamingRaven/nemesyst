.. _page_installation:

.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. |git| replace:: git

Installation
============

.. note::

    Certain distributions link ``python`` to ``python2`` and others link it to ``python3``.
    For disambiguation python, pip, and virtualenv shall mean their python v3 versions here, i.e. ``python3``, ``pip3``, ``virtualenv3``.

.. note::

    You will need to have |git|_ installed for most below methods to work.

.. _section_automated:

Automated
*********

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

To install Nemesyst and all its dependancies into a virtual environment while it is being used (activated):

.. code-block:: bash

    pip install git+https://github.com/DreamingRaven/nemesyst.git#branch=master

To exit the virtual environment:

.. code-block:: bash

      deactivate

.. _section_files-only:

Files only/ development
***********************

.. |minimal_requirements| replace:: ``nemesyst/requirements.txt``

.. |maximal_requirements| replace:: ``nemesyst/docs/requirements.txt``

Nemesyst minimally requires |minimal_requirements|:

.. literalinclude:: ../../requirements.txt

All other methods will automatically install the requirements, however if you would rather just use the files as is without installation you will need to ensure these are installed.

.. note::

  To build the Nemesyst documentation and full testing requires |maximal_requirements|:

  .. literalinclude:: ../requirements.txt

Then just simply:

.. code-block:: bash

    git clone https://github.com/DreamingRaven/nemesyst

We also have a two testers one ``unit_test.py`` for the nemesyst code only, then we also have ``tests/test_everything.sh`` which will test building the documentation, PKGBUILD, nemesyst, etc
