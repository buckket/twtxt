.. _usage:

Usage
=====

twtxt features an excellent command-line interface thanks to `click <http://click.pocoo.org/>`_. Don’t hesitate to append ``--help`` or call commands without arguments to get information about all available commands, options and arguments.

Here are a few of the most common operations you may encounter when using twtxt:

Follow a source
---------------

.. code-block:: console

    $ twtxt follow bob http://bobsplace.xyz/twtxt
    ✓ You’re now following bob.

List all sources you’re following
---------------------------------

.. code-block:: console

    $ twtxt following
    ➤ alice @ https://example.org/alice.txt
    ➤ bob @ http://bobsplace.xyz/twtxt

Unfollow a source
-----------------

.. code-block:: console

    $ twtxt unfollow bob
    ✓ You’ve unfollowed bob.

Post a status update
--------------------

.. code-block:: console

    $ twtxt tweet "Hello, this is twtxt!"

View your timeline
------------------

.. code-block:: console

    $ twtxt timeline

    ➤ bob (5 minutes ago):
    This is my first "tweet". :)

    ➤ alice (2 hours ago):
    I wonder if this is a thing?

View feed of specific source
----------------------------

.. code-block:: console

    $ twtxt view twtxt

    ➤ twtxt (a day ago):
    Fiat Lux!

.. code-block:: console

    $ twtxt view http://example.org/twtxt.txt

    ➤ http://example.org/twtxt.txt (a day ago):
    Fiat Lux!

Edit twtxt configuration
------------------------

.. code-block:: console

    $ twtxt config twtxt.nick tuxtimo
    $ twtxt config twtxt.nick
    tuxtimo
    $ twtxt config --remove twtxt.nick
    $ twtxt config --edit
    # opens your sensible-editor to edit the config file
