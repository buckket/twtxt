.. _api:

API
===

.. module:: twtxt

This chapter documents twtxts API and source code internals.

Tweet Class
-----------

.. autoclass:: models.Tweet
   :members:

   .. attribute:: text

      A :class:`str` representing the message of the tweet.

   .. attribute:: created_at

      A :class:`datetime` representing the creation date of the tweet.
      A value in the future results in an error log.


Source Class
------------

.. autoclass:: models.Source
   :members:

   .. attribute:: nick

      A :class:`str` representing the nick name of the Source.

   .. attribute:: url

      A :class:`str` representing the URL to the sources twtxt file (feed URL).

   .. attribute:: file

      A :class:`str` representing a path to the local twtxt file if available.
      This is attribute is only needed for the users own feed.
