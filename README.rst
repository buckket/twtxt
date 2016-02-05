twtxt
~~~~~
|pypi| |build| |coverage| |gitter| |license|

**twtxt** is a decentralised, minimalist microblogging service for hackers.

So you want to get some thoughts out on the internet? In a convenient and slick way? While also following the gibberish of others? Instead of signing up at a closed and/or regulated microblogging platform, getting your status updates out with twtxt is as easy as putting them in a publicly accessible text file. The URL pointing to this file is your identity, your account. twtxt than can tracks those text files, like a feedreader, and build your unique timeline out of them, depending on which files you track. The format is simple, human readable, and goes well together with all those beloved UNIX command line utilities.

|demo|

**tl;dr**: twtxt is a CLI tool, as well as a format specification for self-hosted flat file based microblogging.

Features
--------
- A beautiful command-line interface thanks to click.
- Asynchronous HTTP requests thanks to asyncio/aiohttp and Python 3.
- Integrates well with existing tools (scp, cut, echo, date, etc.) and your shell.

Installation
------------

Release version:
================
1) Make sure that you have at least Python 3.4.1 installed.

2) Afterwards install this package simply via pip:

.. code::

    $ pip3 install twtxt

3) Now run ``twtxt quickstart``. :)

Development version:
====================
1) Clone the git repository:

.. code::

    $ git clone https://github.com/buckket/twtxt.git

2) Install the package via pip in developer mode:

.. code::

    $ pip3 install -e twtxt/

Usage
-----
**twtxt** features an excellent command-line interface thanks to `click <http://click.pocoo.org/>`_. Don’t hesitate to append ``--help`` or call commands without arguments to get information about all available commands, options and arguments.

Here are a few of the most common operations you may encounter when using **twtxt**:

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

Configuration
-------------
twtxt uses a simple INI-like configuration file. It’s recommended to use ``twtxt quickstart`` to create one. On Linux twtxt checks ``~/.config/twtxt/config`` for it’s configuration. Consult `appdirs <https://github.com/ActiveState/appdirs>`_ to find out the config directory for other operating systems.

Here’s an example ``conf`` file, showing every supported option:

.. code::

    [twtxt]
    nick = buckket
    twtfile = ~/twtxt.txt
    check_following = True
    use_pager = False
    limit_timeline = 20
    post_tweet_hook = "scp {twtfile} buckket@example.org:~/public_html/twtxt.txt"

    [following]
    bob = https://example.org/bob.txt
    alice = https://example.org/alice.txt


twtxt section:
==============
+-------------------+-------+----------+---------------------------------------------------+
| Option:           | Type: | Default: | Help:                                             |
+===================+=======+==========+===================================================+
| nick              | TEXT  |          | your nick, will be displayed in your the timeline |
+-------------------+-------+----------+---------------------------------------------------+
| twtfile           | PATH  |          | path to your local twtxt file                     |
+-------------------+-------+----------+---------------------------------------------------+
| check_following   | BOOL  | True     | try to resolve URLs when listing followings       |
+-------------------+-------+----------+---------------------------------------------------+
| use_pager         | BOOL  | False    | use a pager (less) to display timeline            |
+-------------------+-------+----------+---------------------------------------------------+
| limit_timeline    | INT   | 20       | limit amount of tweets shown in your timeline     |
+-------------------+-------+----------+---------------------------------------------------+
| post_tweet_hook   | TEXT  |          | command to be executed after tweeting             |
+-------------------+-------+----------+---------------------------------------------------+

followings section:
===================
This section holds all your followings as nick, URL pairs. You can edit this section manually or use the ``follow``/``unfollow`` command of twtxt for greater comfort.

Format specification:
---------------------
The central component of sharing information, i.e. status updates, with **twtxt** is a simple text file containing all the status updates of a single user. One status per line, each of which is equipped with an ISO 8601 date/time string followed by a TAB character (\\t) to separate it from the actual text. A specific ordering of the statuses is not mandatory.

The file must be encoded with UTF-8, and must use LF (\\n) as line separators.

A status should consist of up to 140 characters, longer status updates are technically possible but discouraged. **twtxt** will warn the user if a newly composed status update exceeds this limit, and it will also shorten incoming status updates by default. Also note that a status may not contain any control characters.

Take a look at this example file:

.. code::

    2016-02-04T13:30+01	You can really go crazy here! ┐(ﾟ∀ﾟ)┌
    2016-02-01T11:00+01	This is just another example.
    2015-12-12T12:00+01	Fiat lux!


.. |pypi| image:: https://img.shields.io/pypi/v/twtxt.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/twtxt
    :alt: Latest version released on PyPi

.. |build| image:: https://img.shields.io/travis/buckket/twtxt/master.svg?style=flat
    :target: http://travis-ci.org/buckket/twtxt
    :alt: Build status of the master branch

.. |coverage| image:: https://img.shields.io/coveralls/buckket/twtxt/master.svg?style=flat
    :target: https://coveralls.io/r/buckket/twtxt?branch=master
    :alt: Test coverage

.. |gitter| image:: https://img.shields.io/gitter/room/buckket/twtxt.svg?style=flat
    :target: https://gitter.im/buckket/twtxt
    :alt: Chat on gitter

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/buckket/twtxt/master/LICENSE
    :alt: Package license

.. |demo| image:: https://asciinema.org/a/1w2q3suhgrzh2hgltddvk9ot4.png
    :target: https://asciinema.org/a/1w2q3suhgrzh2hgltddvk9ot4
    :alt: Demo
