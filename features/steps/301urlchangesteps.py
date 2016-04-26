from behave import *
import twtxt.models
import twtxt.twhttp
import twtxt.config
import twtxt.cli
import twtxt.cache
import asyncio
import aiohttp
from twtxt.helper import generate_user_agent
@given("a source with a valid nickname and expired URL")
def step_impl(context):
    context.ctx=twtxt.config.Config.discover()
    context.name="patrick"
    context.url="http://127.0.0.1:8081/"
    context.source=twtxt.models.Source(context.name,context.url)
    context.ctx.add_source(context.source)
@when("program attempts to get tweets fromm remote source")
def step_impl(context):
        cache=twtxt.cache.Cache.discover()
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            s=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,context.source,30,cache))
@then("the Source's url will be changed to the new url")
def step_impl(context):
    source=context.ctx.get_source_by_nick("mdom")
    assert (source.url is not "http://127.0.0.1:8081/")

@given("a source with a valid nickname and URL")
def step_impl(context):
    context.ctx=twtxt.config.Config.discover()
    context.name="mdom"
    context.url="https://mdom.github.io/twtxt.txt"
    context.source=twtxt.models.Source(context.name,context.url)
    context.ctx.add_source(context.source)

@when("users views tweets")
def step_impl(context):
        cache=twtxt.cache.Cache.discover()
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            s=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,context.source,30,cache))
@then("the source's url will still be unchanged")
def step_impl(context):
    source=context.ctx.get_source_by_nick("mdom")
    assert (source.url=="https://mdom.github.io/twtxt.txt")
