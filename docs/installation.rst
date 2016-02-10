.. _installation:

Installation
============

The following sections describe how to install twtxt in different ways on your machine.

Requirements:

- Python version > **3.4.1**
- Installed version of pip

Release version
---------------

Install twtxt using pip:

.. code::

    $ pip3 install twtxt

*Tip*: Instead of installing the package globally (as root), you may want to install this package locally by passing ``--user`` to pip, make sure that you include ``~/.local/bin/`` in your ``$PATH``. Using pyvenv and running twtxt from within a virtualenv is also an option!

Development version
-------------------

Clone the git repository:

.. code::

    $ git clone https://github.com/buckket/twtxt.git

We recommend you to develop inside a virtualenv:

.. code::

    $ virtualenv env -p python3.4
    ...
    $ source env/bin/activate

Install the package via pip in developer mode:

.. code::

    $ pip3 install -e twtxt/
