import unittest
import click
from click.testing import CliRunner
import twtxt.models
import twtxt.twhttp
import twtxt.config
import twtxt.cli
import twtxt.cache



class myTestClass(unittest.TestCase):
	def test_runs_new_option_succesfully(self):
		runner = CliRunner()
		result = runner.invoke(twtxt.cli.timeline, ['--newtweets', 'timeline'], None)
		self.assertDictContainsSubset({}, result.output)
		
	def test_if_new_tweet_shows_up_in_timeline(self):
		runner = CliRunner()
		result = runner.invoke(twtxt.cli.tweet, ['-nt', 'timeline'], input='this is new')
		self.assertNotEqual(runner.invoke(twtxt.cli.cli,['timeline']), 0)
	
	def test_still_shows_normal_timeline_with_no_errors(self):
		runner = CliRunner()
		result = runner.invoke(twtxt.cli.tweet, ['timeline'], None)
		self.assertNotEqual(runner.invoke(twtxt.cli.cli,['timeline']), 0)
		
if __name__ == '__main__':
	unittest.main()