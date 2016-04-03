twtxt
~~~~~
|pypi| |build| |coverage| |docs| |gitter| |license|

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

- twtxt gitter chat: https://gitter.im/buckket/twtxt
- twtxt IRC channel: **#twtxt** on `irc.freenode.net`_

Contributions
-------------

- A web-based directory of twtxt users by `reednj <https://twitter.com/reednj>`_: http://twtxt.reednj.com/
- A web-based directory of twtxt users by `xena <https://git.xeserv.us/xena>`_: https://twtxtlist.cf
- A web-based twtxt feed hoster for the masses by `plomlompom <http://www.plomlompom.de/>`_: https://github.com/plomlompom/htwtxt
- A twtxt-to-atom converter in sh by `erlehmann <http://news.dieweltistgarnichtso.net/>`_: http://news.dieweltistgarnichtso.net/bin/twtxt2atom
- A twitter-to-twtxt converter in node.js by `DracoBlue <https://github.com/DracoBlue>`_: https://gist.github.com/DracoBlue/488466eaabbb674c636f
- A port to node.js / npm by `Melvin Carvalho <https://github.com/melvincarvalho>`_: https://github.com/webize/twtxt
- A patched version of TweetNest, which serves TweetNest archives in twtxt format, by `texttheater <https://github.com/texttheater>`_: https://github.com/texttheater/tweetnest/tree/feat/twtxt
- A twtxt registry api by `DracoBlue <https://github.com/DracoBlue>`_: https://registry.twtxt.org
- A twtxt client written in perl by `mdom <https://github.com/mdom>`_: https://github.com/mdom/txtnix
- A web-based directory and registry by `mdom <https://github.com/mdom>`_: http://roster.twtxt.org

License
-------

twtxt is released under the MIT License. See the bundled LICENSE file for details.


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

.. |docs| image:: https://readthedocs.org/projects/twtxt/badge/?version=latest
    :target: http://twtxt.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. _irc.freenode.net: https://freenode.net/
