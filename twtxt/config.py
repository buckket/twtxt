import os
import configparser

from appdirs import user_config_dir
from cached_property import cached_property

from twtxt.types import Source


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
        config_dir = user_config_dir("twtxt", "buckket")
        config_file = "config"

        path = os.path.join(config_dir, config_file)
        return cls.from_file(path)

    def open_config(self):
        cfg = configparser.ConfigParser()
        cfg.read(self.config_file)
        return cfg

    @cached_property
    def following(self):
        cfg = self.open_config()

        following = []
        try:
            for (nick, url) in cfg.items("following"):
                source = Source(nick, url)
                following.append(source)
        except configparser.NoSectionError:
            pass

        return following

    @cached_property
    def twtxt_file(self):
        cfg = self.open_config()
        return cfg.get("twtxt", "file")

    @cached_property
    def twtxt_nick(self):
        cfg = self.open_config()
        return cfg.get("twtxt", "nick")
