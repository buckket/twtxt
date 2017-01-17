.. _quickstart:

Quickstart
==========

Use twtxt's **quickstart** command to bootstrap a default configuration:

.. code-block:: console

    $ twtxt quickstart

    twtxt - quickstart
    ==================

    This wizard will generate a basic configuration file for twtxt with all
    mandatory options set. You can change all of these later with either twtxt
    itself or by editing the config file manually. Have a look at the docs to get
    information about the other available options and their meaning.


    ➤ Please enter your desired nick [$USER]: <NICKNAME>
    ➤ Please enter the desired location for your config
        file [~/.config/twtxt/config]: <CONFIG FILE LOCATION>
    ➤ Please enter the desired location for your twtxt
        file [~/twtxt.txt]: <TWTXTX FILE LOCATION>
    ➤ Please enter the URL your twtxt file will be accessible
        from [https://example.org/twtxt.txt]: <TWTXT URL>
    ➤ Do you want to disclose your identity?
        Your nick and URL will be shared when making HTTP requests [y/N]: y

    ➤ Do you want to follow the twtxt news feed? [Y/n]: y

    ✓ Created config file at '~/.config/twtxt/config'.
    ✓ Created twtxt file at '~/twtxt.txt'.

The quickstart wizard prompts for the following configuration values:

- Your desired nick name, doesn’t need to be unique (*<NICKNAME>*)
- The desired location for your config file (*<CONFIG FILE LOCATION>*)
- The desired location for your twtxt file (*<TWTXTX FILE LOCATION>*)
- The URL your twtxt file will be accessible from remotely (*<TWTXT URL>*)
- If you want to disclose your identity. If True your nick and URL will be used in the User-Agent
  header attribute when fetching other twtxt files via HTTP, see :ref:`discoverability`.
- If you want to follow the official twtxt news feed

The configurations can easily be changed in the twtxt configuration file. See :ref:`configuration`.
