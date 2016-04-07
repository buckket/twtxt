import configparser
import os

import pytest

from twtxt.config import Config
from twtxt.models import Source


@pytest.fixture(scope="session")
def config_dir(tmpdir_factory):
    cfg = configparser.ConfigParser()

    cfg.add_section("twtxt")
    cfg.set("twtxt", "nick", "foo")
    cfg.set("twtxt", "twtfile", "~/foo.txt")
    cfg.set("twtxt", "twturl", "https://axample.org/twtxt.txt")
    cfg.set("twtxt", "check_following", "False")
    cfg.set("twtxt", "use_pager", "True")
    cfg.set("twtxt", "use_cache", "False")
    cfg.set("twtxt", "porcelain", "True")
    cfg.set("twtxt", "character_limit", "150")
    cfg.set("twtxt", "character_warning", "150")
    cfg.set("twtxt", "disclose_identity", "True")
    cfg.set("twtxt", "limit_timeline", "50")
    cfg.set("twtxt", "timeline_update_interval", "20")
    cfg.set("twtxt", "timeout", "1.0")
    cfg.set("twtxt", "sorting", "ascending")
    cfg.set("twtxt", "post_tweet_hook", "echo {twtfile")
    cfg.set("twtxt", "pre_tweet_hook", "echo {twtfile")

    cfg.add_section("following")
    cfg.set("following", "foo", "https://example.org/foo.twtxt")

    config_dir = tmpdir_factory.mktemp("config")

    Config.config_dir = str(config_dir)
    with open(str(config_dir.join(Config.config_name)), "w") as config_file:
        cfg.write(config_file)

    # Manually create an invalid config file.
    with open(str(config_dir.join("config_sanity")), "w") as config_file:
        config_file.write("[twtxt]\n")
        config_file.write("nick = altoyr\n")
        config_file.write("twtfile = ~/twtxt.txt\n")
        config_file.write("check_following = TTrue\n")
        config_file.write("use_pager = Falste\n")
        config_file.write("use_cache = Trute\n")
        config_file.write("porcelain = Faltse\n")
        config_file.write("disclose_identity = Ftalse\n")
        config_file.write("limit_timeline = 2t0\n")
        config_file.write("timeout = 5t.0\n")
        config_file.write("sorting = destcending\n")
        config_file.write("[following]\n")
        config_file.write("twtxt = https://buckket.org/twtxt_news.txt\n")

    return config_dir


def test_defaults():
    empty_cfg = configparser.ConfigParser()
    empty_conf = Config("foobar", empty_cfg)

    assert empty_conf.nick == os.environ.get("USER", "")
    assert empty_conf.twtfile == "twtxt.txt"
    assert empty_conf.twturl is None
    assert empty_conf.check_following is True
    assert empty_conf.use_pager is False
    assert empty_conf.use_cache is True
    assert empty_conf.porcelain is False
    assert empty_conf.character_limit is None
    assert empty_conf.character_warning is None
    assert empty_conf.disclose_identity is False
    assert empty_conf.limit_timeline == 20
    assert empty_conf.timeline_update_interval == 10
    assert empty_conf.timeout == 5.0
    assert empty_conf.sorting == "descending"
    assert empty_conf.post_tweet_hook is None
    assert empty_conf.pre_tweet_hook is None


def check_cfg(cfg):
    assert cfg.nick == "foo"
    assert cfg.twtfile == os.path.expanduser("~/foo.txt")
    assert cfg.twturl == "https://axample.org/twtxt.txt"
    assert cfg.check_following is False
    assert cfg.use_pager is True
    assert cfg.use_cache is False
    assert cfg.porcelain is True
    assert cfg.character_limit == 150
    assert cfg.character_warning == 150
    assert cfg.disclose_identity is True
    assert cfg.limit_timeline == 50
    assert cfg.timeline_update_interval == 20
    assert cfg.timeout == 1.0
    assert cfg.sorting == "ascending"
    assert cfg.post_tweet_hook == "echo {twtfile"
    assert cfg.pre_tweet_hook == "echo {twtfile"
    assert cfg.check_config_sanity() == True


def test_from_file(config_dir):
    with pytest.raises(ValueError) as e:
        Config.from_file("invalid")
    assert "Config file not found." in str(e.value)

    with open(str(config_dir.join("empty")), "a") as fh:
        fh.write("XXX")
    with pytest.raises(ValueError) as e:
        Config.from_file(str(config_dir.join("empty")))
    assert "Config file is invalid." in str(e.value)

    conf = Config.from_file(str(config_dir.join(Config.config_name)))
    check_cfg(conf)


def test_discover():
    conf = Config.discover()
    check_cfg(conf)


def test_create_config(config_dir):
    config_dir_old = Config.config_dir
    Config.config_dir = str(config_dir.join("new"))
    conf_w = Config.create_config(os.path.join(Config.config_dir, Config.config_name),
                                  "bar", "batz.txt", "https://example.org", False, True)
    conf_r = Config.discover()
    assert conf_r.nick == "bar"
    assert conf_r.twtfile == "batz.txt"
    assert conf_r.twturl == "https://example.org"
    assert conf_r.character_limit == 140
    assert conf_r.character_warning == 140
    assert conf_r.following[0].nick == "twtxt"
    assert conf_r.following[0].url == "https://buckket.org/twtxt_news.txt"
    assert set(conf_r.options.keys()) == {"nick", "twtfile", "twturl", "disclose_identity", "character_limit",
                                          "character_warning"}

    conf_r.cfg.remove_section("twtxt")
    assert conf_r.options == {}

    conf_r.cfg.remove_section("following")
    assert conf_r.following == []
    Config.config_dir = config_dir_old


def test_add_get_remove_source():
    conf = Config.discover()
    conf.cfg.remove_section("following")

    assert conf.remove_source_by_nick("foo") is False
    assert conf.get_source_by_nick("baz") is None

    conf.add_source(Source("foo", "bar"))
    source = conf.get_source_by_nick("foo")
    assert source.nick == "foo"
    assert source.url == "bar"

    assert conf.remove_source_by_nick("baz") is False
    assert conf.remove_source_by_nick("foo") is True
    assert conf.following == []


def test_build_default_map():
    empty_cfg = configparser.ConfigParser()
    empty_conf = Config("foobar", empty_cfg)

    default_map = {
        "following": {
            "check": empty_conf.check_following,
            "timeout": empty_conf.timeout,
            "porcelain": empty_conf.porcelain,
        },
        "tweet": {
            "twtfile": empty_conf.twtfile,
        },
        "timeline": {
            "pager": empty_conf.use_pager,
            "cache": empty_conf.use_cache,
            "limit": empty_conf.limit_timeline,
            "timeout": empty_conf.timeout,
            "sorting": empty_conf.sorting,
            "porcelain": empty_conf.porcelain,
            "twtfile": empty_conf.twtfile,
            "update_interval": empty_conf.timeline_update_interval,
        },
        "view": {
            "pager": empty_conf.use_pager,
            "cache": empty_conf.use_cache,
            "limit": empty_conf.limit_timeline,
            "timeout": empty_conf.timeout,
            "sorting": empty_conf.sorting,
            "porcelain": empty_conf.porcelain,
            "update_interval": empty_conf.timeline_update_interval,
        }
    }

    assert empty_conf.build_default_map() == default_map


def test_check_config_file_sanity(capsys, config_dir):
    with pytest.raises(ValueError) as e:
        Config.from_file(str(config_dir.join("config_sanity")))
    assert "Error in config file." in str(e.value)

    out, err = capsys.readouterr()
    for line in ["✗ Config error on limit_timeline - invalid literal for int() with base 10: '2t0'",
                 "✗ Config error on check_following - Not a boolean: TTrue",
                 "✗ Config error on porcelain - Not a boolean: Faltse",
                 "✗ Config error on disclose_identity - Not a boolean: Ftalse",
                 "✗ Config error on timeout - could not convert string to float: '5t.0'",
                 "✗ Config error on use_pager - Not a boolean: Falste",
                 "✗ Config error on use_cache - Not a boolean: Trute"]:
        assert line in out
