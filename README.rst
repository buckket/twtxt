twtxt
~~~~~

twtxt is a decentralised, minimalist microblogging service for hackers.
Features
--------
- Search autocompletion (uses DeckBrew API)
- Loading and saving decks as plain text files
- Sample hand window, including mulligans button
- Mana curve plot shows colored mana requirements

Screenshot
----------
.. image:: https://uncloaked.net/~loom/stuff/mtg_deck_editor.png

Installation
------------
1) Under Debian GNU/Linux, install major dependencies with:

.. code:: bash

    $ apt-get install gir1.2-gtk-3.0 python-gi-cairo python-matplotlib

2) Afterwards install this package simply via pip.

.. code:: bash

    $ pip install mtg-deck-editor

3) Now run ``mtg-deck-editor``. :)


Format specification:
---------------------
The central component of sharing information, i.e. status updates, with twtxt is a simple text file containing all the status updates of a single user. One status per line, each of which is equipped with an unix timestamp. A specific ordering is not mandatory, but it’s recommended to put the newest status at the beginning of the file, so that humans can parse the new content more easily. The file should be encoded with UTF-8, and must use LF (\n) as line separators (unix-style). A status should consist of up to 140 characters, longer status updates are technically possible but discouraged. twtxt will warn the user if a newly composed status update exceeds this limit, and it will also shorten incoming status updates by default. Take a look at this example file:

.. code::

    1454287712: You can really go crazy here! ┐(ﾟ∀ﾟ)┌ ?
    1454243768: Python 3 is a superb programming language. ;)
    1454243968: This is just another example.
    1454252639: Fiat Lux!

Links
-----
- `website (upstream) <http://news.dieweltistgarnichtso.net/bin/mtg-deck-editor.html>`_
- `development version <https://github.com/buckket/mtg-deck-editor>`_