import unittest
import aiohttp
import click
import ssl
from click.testing import CliRunner
import twtxt.models
import twtxt.twhttp
import twtxt.config
import twtxt.cli


class MyTestCase(unittest.TestCase):
    def test_301url_reroute(self):
        config=twtxt.config.Config.discover()
        name="patrick"
        url="testfilefor301redirect.html"
        source=twtxt.models.Source(name,url)
        config.add_source(source)
        with aiohttp.ClientSession() as client:
            twtxt.twhttp.retrieve_file(client,source,30,config)
        newSOurce=config.get_source_by_nick(name)
        self.assertNotEqual(newSOurce.url,url)
    def test_301reroute_doesnot_effectgodpasswords(self):
        config=twtxt.config.Config.discover()
        name="mdom"
        url="https://mdom.github.io/twtxt.txt"
        source=twtxt.models.Source(name,url)
        config.add_source(source)
        with aiohttp.ClientSession() as client:
            twtxt.twhttp.retrieve_file(client,source,30,config)
        newSOurce=config.get_source_by_nick(name)
        self.assertEqual(newSOurce.url,url)
    def test_aiohttpdoesnotCrashProgramWhenSOurceCannotBeRead(self):

        runner = CliRunner()
        self.assertEqualsrunner.invoke(twtxt.cli.cli,['timeline'])

    def test_iferroristhrownWhenConnectingToPageWithBadCertificate(self):
        config=twtxt.config.Config.discover()
        name="mdom"
        url="https://expired.badssl.com/"
        source=twtxt.models.Source(name,url)
        config.add_source(source)
        with aiohttp.ClientSession() as client:
            self.assertRaises(aiohttp.errors.ClientOSError,twtxt.twhttp.retrieve_file,client,source,30,config)







if __name__ == '__main__':
    unittest.main()
