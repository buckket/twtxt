from behave import *
import twtxt.models
import twtxt.twhttp
import twtxt.config
import twtxt.cli
import asyncio
import aiohttp
from twtxt.cache import Cache


@given("a source <username> at <url> is provided")
def step_impl(context):
    context.ctx=twtxt.config.Config.discover()
    context.name="mdom"
    context.url="https://kdave.github.io/twtxt-test.txt"
    context.tweets=[]
    context.source=twtxt.models.Source(context.name,context.url)
@when("the program tries to retrieve tweets from a remote source")
def step_impl(context):
    with aiohttp.ClientSession() as client:
        loop = asyncio.get_event_loop()

        def start_loop(client, sources, limit, cache=None):
            return loop.run_until_complete(twtxt.twhttp.process_sources_for_file(client, sources, limit, cache))
        try:
            with Cache.discover() as cache:
                context.tweets=start_loop(client, [context.source], 7, cache)
        except Exception as caughtexception:
            context.error=caughtexception
@then("a list of tweets with a length greater than 0 should be returned")
def step_impl(context):
    assert(len(context.tweets)>0)