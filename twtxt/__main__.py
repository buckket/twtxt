#!/usr/bin/env python3

"""
    twtxt.__main__
    ~~~~~~~~~~~~~~

    Alias for twtxt.cli for the command line.

    :copyright: (c) 2016-2022 by buckket.
    :license: MIT, see LICENSE for more details.
"""

if __name__ == '__main__':
    import sys
    import twtxt.cli
    sys.exit(twtxt.cli.main())
