.. _discoverability:

Discoverability
===============

Because of the decentral nature of twtxt it can be hard to find new peers to follow, or even know who is following one’s own feed.
The later being a problem because right now mentions only show up when you actively follow the feed the mention originated from.

To solve this issue, besides the usage of :ref:`registries <registry>`, twtxt is using a specially crafted User-Agent string, when making outgoing HTTP requests.
This then allows other users to search their webserver’s log file for those strings and find out who is consuming their content.

.. note::

    Implementing a so called linkback mechanism to actively notify someone explicitly about incoming mentions is currently `being discussed on GitHub <https://github.com/buckket/twtxt/issues/109>`_.

The format twtxt is using is as follows:

.. code::

    twtxt/<version> (+<source.url>; @<source.nick>)

For example:

.. code::

    twtxt/1.2.3 (+https://example.com/twtxt.txt; @somebody)

Other clients are encouraged to use the same format.
