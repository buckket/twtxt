.. twtxtfile:

twtxt file
==========

The central component of sharing information, i.e. status updates, with twtxt is a simple text file containing all the status updates of a single user. This file is often referred as the *feed* of an user.
The location of the twtxt file is configured in the twtxt section in the configuration file. See :ref:`configuration`.

Format specification
--------------------

The twtxt file contains one status per line, each of which is equipped with an RFC 3339 date-time string (with or without UTC offset) followed by a TAB character (\\t) to separate it from the actual text. A specific ordering of the statuses is not mandatory.

The file must be encoded with UTF-8 and must use LF (\\n) as line separators.

A status should consist of up to 140 characters, longer status updates are technically possible but discouraged. twtxt will warn the user if a newly composed status update exceeds this limit, and it will also shorten incoming status updates by default. Also note that a status may not contain any control characters.

Mentions are embedded within the text in either `@<source.nick source.url>` or `@<source.url>` format and should be expanded by the client, when rendering the tweets. The `source.url` is available to provide a way to discover new `twtxt.txt` files and distinguish between multiple users using the same nickname locally. The `source.url` can be interpreted as a TWTXT URI.

Take a look at this example file:

.. code::

    2016-02-04T13:30:00+01:00	You can really go crazy here! ┐(ﾟ∀ﾟ)┌
    2016-02-03T23:05:00+01:00	@<example http://example.org/twtxt.txt> welcome to twtxt!
    2016-02-01T11:00:00+01:00	This is just another example.
    2015-12-12T12:00:00+01:00	Fiat lux!
