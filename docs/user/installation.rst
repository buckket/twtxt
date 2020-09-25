.. _installation:

Installation
============

The following sections describe how to install twtxt in different ways on your machine. Currently the we support Windows, Mac OS X and Linux via pip_.

**Requirements**:

- Python_ >= **3.4.1**
- Recent version of pip_

Release version
---------------

Install twtxt using pip_:

.. code-block:: console

    $ pip3 install twtxt

.. note::

    Instead of installing the package globally (as root), you may want to install this package locally by passing ``--user`` to pip,
    make sure that you append ``~/.local/bin/`` to your ``$PATH``. You may also install it using ``pipx`` with ``pipx install twtxt``. Or use ``pyvenv`` and run ``twtxt`` from within a virtualenv.


Packages exist for the following systems:

- `Arch Linux (AUR) <https://aur.archlinux.org/packages/twtxt/>`_
- `Mac OS X (homebrew) <http://braumeister.org/formula/twtxt>`_

Development version
-------------------

Clone the git_ repository:

.. code-block:: console

    $ git clone https://github.com/buckket/twtxt.git

We recommend you to develop inside a virtualenv:

.. code-block:: console

    $ pyvenv env
        ...
    $ source env/bin/activate

Install the package via pip_ in developer mode:

.. code-block:: console

    $ pip3 install -e twtxt/[dev]

.. note::

    Appending ``[dev]`` to the package name or target location will also install the packages required for testing twtxt,
    by making use of `setuptool’s extra <https://pythonhosted.org/setuptools/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies>`_ functionality.


.. _Python: https://www.python.org/
.. _pip: http://pip-installer.org/
.. _git: https://git-scm.com/
