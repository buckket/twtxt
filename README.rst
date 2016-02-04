twtxt
~~~~~

*twtxt* is a decentralised, minimalist microblogging service for hackers.

Installation
------------

Release version:
================
1) Make sure that you have at least Python 3.4.1 installed.

2) Afterwards install this package simply via pip:

.. code::

    $ pip install twtxt

3) Now run ``twtxt``. :)

Development version:
====================
1) Clone the repository:

.. code::

    $ git clone https://github.com/buckket/twtxt.git

2) Install the package via pip in developer mode:

.. code::

    $ pip install -e twtxt/


Usage
-----
*twtxt* features an excellent command-line interface thanks to `click <http://click.pocoo.org/>`_. Don’t hesitate to append ``--help`` to get information about all available commands, options and arguments.

Here are a few of the most common operations you encounter when using twtxt:

Follow a source:
================

.. code::

    $ twtxt follow bob http://bobsplace.xyz/twtxt
    ✓ You’re now following bob.

List all sources you’re following:
==================================

.. code::

    $ twtxt following
    ➤ alice @ https://example.org/alice.txt
    ➤ bob @ http://bobsplace.xyz/twtxt

Unfollow a source:
==================

.. code::

    $ twtxt unfollow bob
    ✓ You’ve unfollowed bob.

Post a status update:
=====================

.. code::

    $ twtxt tweet "Hello, this is twtxt!"

View your timeline:
===================

.. code::

    $ twtxt timeline

    ➤ bob (5 minutes ago):
    This is my first "tweet". :)

    ➤ alice (2 hours ago):
    I wonder if this is a thing?

Format specification:
---------------------
The central component of sharing information, i.e. status updates, with *twtxt* is a simple text file containing all the status updates of a single user. One status per line, each of which is equipped with an ISO 8601 date/time string followed by a TAB (\\t) to separate it from the actual text. A specific ordering of the statuses is not mandatory. The file must be encoded with UTF-8, and must use LF (\\n) as line separators. A status should consist of up to 140 characters, longer status updates are technically possible but discouraged. twtxt will warn the user if a newly composed status update exceeds this limit, and it will also shorten incoming status updates by default. Also note that a status may not contain any control characters. Take a look at this example file:

.. code::

    2016-02-04T13:30+01	You can really go crazy here! ┐(ﾟ∀ﾟ)┌
    2016-02-01T11:00+01	This is just another example.
    2015-12-12T12:00+01	Fiat lux!
