.. _registry:

Registry
========

Since twtxt is decentralized by design, features like the timeline are limited to the twtxt users followed by you. To
provide a global search for mentions or hash tags, the client will be able to query so called registries.

A reference implementation is available at `twtxt-registry (source)`_ in nodejs and
a demo instance is running at `twtxt-registry (demo)`_.

The client will support multiple registries at the same time, to circumvent possible single point of failures. The
registries should sync each others user list by using the `users` endpoint.

Format specification
--------------------

**Writing to the registry**

The responses return proper status code (200 OK) and the description of the status code or a
detailed error message.

**Reading from the registry**

The responses contain one status per line, each of which is equipped with nick of the
poster followed by a TAB, the twtxturl of the poster followed by a TAB and an RFC 3339 date-time string followed by a TAB character (\\t) to separate it from the actual
text.

.. code-block:: text

	NICK\tURL\tTIMESTAMP\tMESSAGE

**General rules**

1. All lists are sorted by timestamp in descending order (most recent one first)
2. All lists support the `page` query parameter to get the next page of the result set.
3. The response must be encoded with UTF-8 and must use LF (\\n) as line separators.
4. The columns are separated by a tab character (\\t)

API Endpoints
-------------

The url to the registry consists of its basepath (e.g. `https://registry.twtxt.org/api/`). The format (e.g. `plain`) is
appended, because we might support json or xml format sooner or later.

The following parameters:

* basePath: `https://registry.twtxt.org/api/`
* format: `plain`
* endpoint: `tags/twtxt`

will call this url: `https://registry.twtxt.org/api/plain/tags/twtxt`.

Add new User
------------

Add a new Twtxt User to the Registry (Status Code is 200):

.. code-block:: console

	$ curl -X POST 'https://registry.twtxt.org/api/plain/users?url=https://example.org/twtxt.txt&nickname=example'
	OK

If it fails to add a new Twtxt User to the Registry (Status Code is 400):

.. code-block:: console

	$ curl -X POST 'https://registry.twtxt.org/api/plain/users?url=https://example.org/twtxt.txt'
	Bad Request: `nickname` is missing

Latest tweets
-------------

See latest tweets in the Registry (e.g. <https://registry.twtxt.org/api/plain/tweets>):

.. code-block:: console

	$ curl 'https://registry.twtxt.org/api/plain/tweets'
	example	https://example.org/twtxt.txt	2016-02-06T21:32:02.000Z	@erlehmann is messing with timestamps in @buckket #twtxt :)
	example	https://example.org/twtxt.txt	2016-02-06T12:14:18.000Z	Simple nodejs script to convert your twitter timeline to twtxt: https://t.co/txnWsC5jvA ( find my #twtxt at https://t.co/uN1KDXwJ8B )

Search for tweets
-----------------

To query for tweets, which contain a specific word, use the tweets endpoint and the q query parameter.

.. code-block:: console

	$ curl 'https://registry.twtxt.org/api/plain/tweets?q=twtxt'
	buckket	https://buckket.org/twtxt.txt	2016-02-09T12:42:26.000Z	Do we need an IRC channel for twtxt?
	buckket	https://buckket.org/twtxt.txt	2016-02-09T12:42:12.000Z	Good Morning, twtxt-world!

Query for mentions
------------------

To query for all tweets, which mention a specific user, use the mentions endpoint and the url query parameter.

.. code-block:: console

	$ curl 'https://registry.twtxt.org/api/plain/mentions?url=https://buckket.org/twtxt.txt'
	example	https://example.org/twtxt.txt	2016-02-09T12:57:59.000Z	@<buckket https://buckket.org/twtxt.txt> something like https://gitter.im/ or a freenode channel?
	example	https://example.org/twtxt.txt	2016-02-08T22:51:47.000Z	@<buckket https://buckket.org/twtxt.txt> looks nice ;)

Query for tags
--------------

To query for all tweets, which contain a specific tag like `#twtxt`, use the tags endpoint and prepend the tag.

.. code-block:: console

	$ curl 'https://registry.twtxt.org/api/plain/tags/twtxt'
	example	https://example.org/twtxt.txt	2016-02-06T21:32:02.000Z	@erlehmann is messing with timestamps in @buckket #twtxt :)
	example	https://example.org/twtxt.txt	2016-02-06T12:14:18.000Z	Simple nodejs script to convert your twitter timeline to twtxt: https://t.co/txnWsC5jvA ( find my #twtxt at https://t.co/uN1KDXwJ8B )

Query for users
---------------

To query for a user list, use the users endpoint and refine with the q query parameter.

.. code-block:: console

	$ curl 'https://registry.twtxt.org/api/plain/users?q=example'
	example	https://example.org/twtxt.txt	2016-02-09T12:42:26.000Z
	example42	https://example.org/42.twtxt.txt	2016-02-10T13:20:10.000Z

.. _twtxt-registry (source): https://github.com/DracoBlue/twtxt-registry
.. _twtxt-registry (demo): https://registry.twtxt.org
