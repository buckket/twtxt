"""
    twtxt.config
    ~~~~~~~~~~~~

    This module implements the config file parser/writer.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import click
import configparser
import logging
import os


from twtxt.types import Source

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, config_file):
        self.config_file = config_file

    @classmethod
    def from_file(cls, file):
        if not os.path.exists(file):
            raise ValueError("Config file not found.")

        cfg = configparser.ConfigParser()
        try:
            if cfg.read(file):
                return cls(file)
            else:
                raise ValueError("Config file is empty.")
        except configparser.Error:
            raise ValueError("Config file is invalid.")

    @classmethod
    def discover(cls):
        config_dir = click.get_app_dir("twtxt")
        config_file = "config"
        path = os.path.join(config_dir, config_file)
        return cls.from_file(path)

    def create_config(self, nick, twtfile, add_news):
        config_dir = click.get_app_dir("twtxt")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config_file = "config"
        path = os.path.join(config_dir, config_file)
        self.config_file = path

        cfg = configparser.ConfigParser()

        cfg.add_section("twtxt")
        cfg.set("twtxt", "nick", nick)
        cfg.set("twtxt", "twtfile", twtfile)

        cfg.add_section("following")
        if add_news:
            cfg.set("following", "twtxt", "https://buckket.org/twtxt_news.txt")

        self.write_config(cfg)

    def open_config(self):
        cfg = configparser.ConfigParser()
        cfg.read(self.config_file)
        return cfg

    def write_config(self, cfg):
        with open(self.config_file, "w") as config_file:
            cfg.write(config_file)

    @property
    def following(self):
        cfg = self.open_config()

        following = []
        try:
            for (nick, url) in cfg.items("following"):
                source = Source(nick, url)
                following.append(source)
        except configparser.NoSectionError as e:
            logger.debug(e)

        return following

    @property
    def options(self):
        cfg = self.open_config()
        try:
            return dict(cfg.items("twtxt"))
        except configparser.NoSectionError as e:
            logger.debug(e)
            return {}

    @property
    def nick(self):
        cfg = self.open_config()
        return cfg.get("twtxt", "nick", fallback=os.environ.get("USER", ""))

    @property
    def post_tweet_hook(self):
        cfg = self.open_config()
        return cfg.get("twtxt", "post_tweet_hook", fallback=None)

    @property
    def timeline_sorting(self):
        cfg = self.open_config()
        return cfg.get("twtxt", "timeline_sorting", fallback="descending")

    def add_source(self, source):
        cfg = self.open_config()

        if not cfg.has_section("following"):
            cfg.add_section("following")

        cfg.set("following", source.nick, source.url)
        self.write_config(cfg)

    def remove_source_by_nick(self, nick):
        cfg = self.open_config()

        if not cfg.has_section("following"):
            return False

        ret_val = cfg.remove_option("following", nick)
        self.write_config(cfg)
        return ret_val

    def build_default_map(self):
        cfg = self.open_config()

        twtfile = os.path.expanduser(cfg.get("twtxt", "twtfile", fallback="twtxt.txt"))

        default_map = {
            "following": {
                "check": cfg.get("twtxt", "check_following", fallback=True),
                "timeout": cfg.getfloat("twtxt", "timeout", fallback=5.0),
            },
            "tweet": {
                "twtfile": twtfile,
            },
            "timeline": {
                "pager": cfg.getboolean("twtxt", "use_pager", fallback=False),
                "limit": cfg.getint("twtxt", "limit_timeline", fallback=20),
                "timeout": cfg.getfloat("twtxt", "timeout", fallback=5.0),
                "twtfile": twtfile,
            }
        }

        return default_map
