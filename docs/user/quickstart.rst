.. _quickstart:

Quickstart
==========

Use twtxt's **quickstart** command to bootstrap a default configuration:

.. code-block:: console

    $ twtxt quickstart

    twtxt - quickstart
    ==================

    This wizard will generate a basic configuration file for twtxt
    with all mandatory options set. Have a look at the docs to
    get information about the other available options and their meaning.

    ➤ Please enter your desired nick [$USER]: <NICKNAME>
    ➤ Please enter the desired location for your config
        file [~/.config/twtxt/config]: <CONFIG FILE LOCATION>
    ➤ Please enter the desired location for your twtxt
        file [~/twtxt.txt]: <TWTXTX FILE LOCATION>
    ➤ Do you want to disclose your identity?
        Your nick and URL will be shared [y/N]: y

    ➤ Do you want to follow the twtxt news feed? [Y/n]: y

    ✓ Created config file at '~/.config/twtxt/config'.
    ✓ Created twtxt file at '~/twtxt.txt'.

The quickstart wizard prompts for the following configuration values:

- Your desired nick name (*<NICKNAME>*)
- The desired location for your config file (*<CONFIG FILE LOCATION>*)
- The desired location for your twtxt file (*<TWTXTX FILE LOCATION>*)
- If you want to disclose your identity. If True your nick and URL will be used in the User-Agent
  attribute when fetching other twtxt files.
- If you want to follow the official twtxt news feed

The configurations can easily be changed in the twtxt configuration file. See :ref:`configuration`.
