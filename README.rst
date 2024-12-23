twtxt
~~~~~
|pypi| |build| |coverage| |docs| |license|

**twtxt** is a decentralised, minimalist microblogging service for hackers.

So you want to get some thoughts out on the internet in a convenient and slick way while also following the gibberish of others? Instead of signing up at a closed and/or regulated microblogging platform, getting your status updates out with twtxt is as easy as putting them in a publicly accessible text file. The URL pointing to this file is your identity, your account. twtxt then tracks these text files, like a feedreader, and builds your unique timeline out of them, depending on which files you track. The format is simple, human readable, and integrates well with UNIX command line utilities.


|demo|

**tl;dr**: twtxt is a CLI tool, as well as a format specification for self-hosted flat file based microblogging.

Features
--------

- A beautiful command-line interface thanks to click.
- Asynchronous HTTP requests thanks to asyncio/aiohttp and Python 3.
- Integrates well with existing tools (scp, cut, echo, date, etc.) and your shell.
- Don’t like the official client? Tweet using ``echo -e "`date +%FT%T%:z`\tHello world!" >> twtxt.txt``!

Documentation
-------------

Check out the full documentation at: http://twtxt.readthedocs.org/en/latest/

Community
---------

- twtxt IRC channel: **#twtxt** on `irc.libera.chat`_

Contributions
-------------

- A curated list of active twtxt users by `yarn.social <https://yarn.social/>`_: https://git.mills.io/yarnsocial/we-are-twtxt
- A web-based directory of twtxt users by `reednj <https://twitter.com/reednj>`_: http://twtxt.reednj.com/
- A web-based twtxt feed hoster for the masses by `plomlompom <http://www.plomlompom.de/>`_: https://github.com/plomlompom/htwtxt
- A twtxt-to-atom converter in sh by `erlehmann <http://news.dieweltistgarnichtso.net/>`_: http://news.dieweltistgarnichtso.net/bin/twtxt2atom
- A twitter-to-twtxt converter in node.js by `DracoBlue <https://github.com/DracoBlue>`_: https://gist.github.com/DracoBlue/488466eaabbb674c636f
- A port to node.js / npm by `Melvin Carvalho <https://github.com/melvincarvalho>`_: https://github.com/webize/twtxt
- A patched version of TweetNest, which serves TweetNest archives in twtxt format, by `texttheater <https://github.com/texttheater>`_: https://github.com/texttheater/tweetnest/tree/feat/twtxt
- A twtxt registry api by `DracoBlue <https://github.com/DracoBlue>`_: https://registry.twtxt.org
- A twtxt client written in perl by `mdom <https://github.com/mdom>`_: https://github.com/mdom/txtnix
- A twtxt client with minimal dependencies by `mdom <https://github.com/mdom>`_: https://github.com/mdom/txtnish
- A twtxt client written in C by `dertuxmalwieder <https://github.com/dertuxmalwieder>`_: https://hub.darcs.net/dertuxmalwieder/twtxtc
- A read-only timeline of the last 3000 tweets via gopher by `trqx <gopher://shroom.party>`_: gopher://shroom.party/1/twtxt
- A bot for using twtxt over xmpp by `mdosch <https://blog.mdosch.de>`_: https://salsa.debian.org/mdosch-guest/goxtxt
- twtxt registry server written in Go by `gbmor <https://github.com/gbmor>`_: https://github.com/gbmor/getwtxt-ng
- A twtxt parsing library written in Rust by `gbmor <https://github.com/gbmor>`_: https://github.com/rustwtxt/rustwtxt
- A twtxt WordPress plugin, that provides the blog-posts as twtxt file, written by `pfefferle <https://github.com/pfefferle>`_: https://github.com/pfefferle/wordpress-twtxt
- A twtxt client for Emacs by `deadblackclover <https://codeberg.org/deadblackclover/twtxt-el>`_: https://codeberg.org/deadblackclover/twtxt-el
- An php interface for publishing to your selfhosted twtxt.txt by `sorenpeter <https://github.com/sorenpeter>`_: https://github.com/sorenpeter/phpub2twtxt/
- A graphical twtxt client written in Tcl/Tk, RSS-to-twtxt converter, and mentions extractor by `dbohdan <https://dbohdan.com>`_: https://gitlab.com/dbohdan/twtxt.tcl
- twtwt: a really fast UNIX only twtxt client written in C by `win0err <https://github.com/win0err>`_: https://github.com/win0err/twtwt



License
-------

twtxt is released under the MIT License. See the bundled LICENSE file for details.


.. |pypi| image:: https://img.shields.io/pypi/v/twtxt.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/twtxt
    :alt: Latest version released on PyPi

.. |build| image:: https://github.com/buckket/twtxt/actions/workflows/python.yml/badge.svg
    :target: https://github.com/buckket/twtxt/actions/workflows/python.yml
    :alt: Build status of the master branch

.. |coverage| image:: https://img.shields.io/coveralls/buckket/twtxt/master.svg?style=flat
    :target: https://coveralls.io/r/buckket/twtxt?branch=master
    :alt: Test coverage

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/buckket/twtxt/master/LICENSE
    :alt: Package license

.. |demo| image:: https://asciinema.org/a/1w2q3suhgrzh2hgltddvk9ot4.png
    :target: https://asciinema.org/a/1w2q3suhgrzh2hgltddvk9ot4
    :alt: Demo

.. |docs| image:: https://readthedocs.org/projects/twtxt/badge/?version=latest
    :target: http://twtxt.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. _irc.libera.chat: https://libera.chat/
