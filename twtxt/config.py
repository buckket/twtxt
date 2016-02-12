"""
    twtxt.config
    ~~~~~~~~~~~~

    This module implements the config file parser/writer.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import configparser
import logging
import os

import click

from twtxt.models import Source

logger = logging.getLogger(__name__)


class Config:
    config_dir = click.get_app_dir("twtxt")
    config_name = "config"

    def __init__(self, config_file, cfg):
        """Initializes new :class:`Config` object.

        :param config_file: full path to the loaded config file.
        :param cfg: a ConfigParser object, with config loaded.
        """
        self.config_file = config_file
        self.cfg = cfg

    @classmethod
    def from_file(cls, file):
        """Try loading given config file."""
        if not os.path.exists(file):
            raise ValueError("Config file not found.")
        cfg = configparser.ConfigParser()
        try:
            cfg.read(file)
            return cls(file, cfg)
        except configparser.Error:
            raise ValueError("Config file is invalid.")

    @classmethod
    def discover(cls):
        """Make a guess about the config file location an try loading it."""
        file = os.path.join(Config.config_dir, Config.config_name)
        return cls.from_file(file)

    @classmethod
    def create_config(cls, nick, twtfile, add_news):
        """Creates a new config file at the default location."""
        if not os.path.exists(Config.config_dir):
            os.makedirs(Config.config_dir)
        file = os.path.join(Config.config_dir, Config.config_name)

        cfg = configparser.ConfigParser()

        cfg.add_section("twtxt")
        cfg.set("twtxt", "nick", nick)
        cfg.set("twtxt", "twtfile", twtfile)

        cfg.add_section("following")
        if add_news:
            cfg.set("following", "twtxt", "https://buckket.org/twtxt_news.txt")

        conf = cls(file, cfg)
        conf.write_config()
        return conf

    def write_config(self):
        """Writes ConfigParser object to file."""
        with open(self.config_file, "w") as config_file:
            self.cfg.write(config_file)

    @property
    def following(self):
        """Returns a list of all source objects."""
        following = []
        try:
            for (nick, url) in self.cfg.items("following"):
                source = Source(nick, url)
                following.append(source)
        except configparser.NoSectionError as e:
            logger.debug(e)

        return following

    @property
    def options(self):
        """Returns a dict of all config options."""
        try:
            return dict(self.cfg.items("twtxt"))
        except configparser.NoSectionError as e:
            logger.debug(e)
            return {}

    @property
    def nick(self):
        return self.cfg.get("twtxt", "nick", fallback=os.environ.get("USER", ""))

    @property
    def twtfile(self):
        return os.path.expanduser(self.cfg.get("twtxt", "twtfile", fallback="twtxt.txt"))

    @property
    def twturl(self):
        return self.cfg.get("twtxt", "twturl", fallback=None)

    @property
    def check_following(self):
        return self.cfg.getboolean("twtxt", "check_following", fallback=True)

    @property
    def use_pager(self):
        return self.cfg.getboolean("twtxt", "use_pager", fallback=False)

    @property
    def use_cache(self):
        return self.cfg.getboolean("twtxt", "use_cache", fallback=True)

    @property
    def porcelain(self):
        return self.cfg.getboolean("twtxt", "porcelain", fallback=False)

    @property
    def limit_timeline(self):
        return self.cfg.getint("twtxt", "limit_timeline", fallback=20)

    @property
    def timeout(self):
        return self.cfg.getfloat("twtxt", "timeout", fallback=5.0)

    @property
    def sorting(self):
        return self.cfg.get("twtxt", "sorting", fallback="descending")

    @property
    def source(self):
        return Source(self.nick, self.twturl)

    @property
    def pre_tweet_hook(self):
        return self.cfg.get("twtxt", "pre_tweet_hook", fallback=None)

    @property
    def post_tweet_hook(self):
        return self.cfg.get("twtxt", "post_tweet_hook", fallback=None)

    def add_source(self, source):
        """Adds a new source to the config’s following section."""
        if not self.cfg.has_section("following"):
            self.cfg.add_section("following")

        self.cfg.set("following", source.nick, source.url)
        self.write_config()

    def get_source_by_nick(self, nick):
        """Returns the source of the given nick."""
        url = self.cfg.get("following", nick, fallback=None)
        return Source(nick, url) if url else None

    def remove_source_by_nick(self, nick):
        """Removes a source form the config’s following section."""
        if not self.cfg.has_section("following"):
            return False

        ret_val = self.cfg.remove_option("following", nick)
        self.write_config()
        return ret_val

    def build_default_map(self):
        """Maps the set options to the default values used by click."""
        default_map = {
            "following": {
                "check": self.check_following,
                "timeout": self.timeout,
                "porcelain": self.porcelain,
            },
            "tweet": {
                "twtfile": self.twtfile,
            },
            "timeline": {
                "pager": self.use_pager,
                "cache": self.use_cache,
                "limit": self.limit_timeline,
                "timeout": self.timeout,
                "sorting": self.sorting,
                "porcelain": self.porcelain,
                "twtfile": self.twtfile,
            },
            "view": {
                "pager": self.use_pager,
                "cache": self.use_cache,
                "limit": self.limit_timeline,
                "timeout": self.timeout,
                "sorting": self.sorting,
                "porcelain": self.porcelain,
            }
        }
        return default_map
