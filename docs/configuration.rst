.. _configuration:

Configuration
=============

twtxt uses a simple INI-like configuration file. It’s recommended to use ``twtxt quickstart`` to create it. On Linux twtxt checks ``~/.config/twtxt/config`` for its configuration. OSX uses ``~/Library/Application Support/twtxt/config``. Consult `get_app_dir <http://click.pocoo.org/6/api/#click.get_app_dir>`_ to find out the config directory for other operating systems.

Here’s an example ``conf`` file, showing every currently supported option:

.. code::

    [twtxt]
    nick = buckket
    twtfile = ~/twtxt.txt
    twturl = http://example.org/twtxt.txt
    check_following = True
    use_pager = False
    porcelain = False
    limit_timeline = 20
    timeout = 5.0
    sorting = descending
    post_tweet_hook = "scp {twtfile} buckket@example.org:~/public_html/twtxt.txt"
    # post_tweet_hook = "aws s3 {twtfile} s3://mybucket.org/twtxt.txt --acl public-read --storage-class REDUCED_REDUNDANCY --cache-control 'max-age=60,public'"

    [following]
    bob = https://example.org/bob.txt
    alice = https://example.org/alice.txt


[twtxt] section
---------------

+-------------------+-------+------------+---------------------------------------------------+
| Option:           | Type: | Default:   | Help:                                             |
+===================+=======+============+===================================================+
| nick              | TEXT  |            | your nick, will be displayed in your timeline     |
+-------------------+-------+------------+---------------------------------------------------+
| twtfile           | PATH  |            | path to your local twtxt file                     |
+-------------------+-------+------------+---------------------------------------------------+
| twturl            | TEXT  |            | URL to your public twtxt file                     |
+-------------------+-------+------------+---------------------------------------------------+
| check_following   | BOOL  | True       | try to resolve URLs when listing followings       |
+-------------------+-------+------------+---------------------------------------------------+
| use_pager         | BOOL  | False      | use a pager (less) to display your timeline       |
+-------------------+-------+------------+---------------------------------------------------+
| porcelain         | BOOL  | False      | style output in an easy-to-parse format           |
+-------------------+-------+------------+---------------------------------------------------+
| limit_timeline    | INT   | 20         | limit amount of tweets shown in your timeline     |
+-------------------+-------+------------+---------------------------------------------------+
| timeout           | FLOAT | 5.0        | maximal time a http request is allowed to take    |
+-------------------+-------+------------+---------------------------------------------------+
| sorting           | TEXT  | descending | sort timeline either descending or ascending      |
+-------------------+-------+------------+---------------------------------------------------+
| post_tweet_hook   | TEXT  |            | command to be executed after tweeting             |
+-------------------+-------+------------+---------------------------------------------------+

``post_tweet_hook`` is very useful if you want to push your twtxt file to a remote (web) server. Check the example above tho see how it’s used with ``scp``.

[followings] section
--------------------

This section holds all your followings as nick, URL pairs. You can edit this section manually or use the ``follow``/``unfollow`` commands of twtxt for greater comfort.
