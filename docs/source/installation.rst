Installation
============

Automated
*********

Generic
+++++++

In future you will be able to:

.. code-block:: bash

  pip install nemesyst

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

Files only/ development
***********************

.. |minimal_requirements| replace:: ``nemesyst/requirements.txt``

.. |maximal_requirements| replace:: ``nemesyst/docs/requirements.txt``

Nemesyst minimally requires |minimal_requirements|:

.. literalinclude:: ../../requirements.txt

All methods below will automatically install the requirements, however if you would rather just use the files as is without installation you will need to ensure these are installed.

.. note::

  To build the Nemesyst documentation and full testing requires |maximal_requirements|:

  .. literalinclude:: ../requirements.txt
