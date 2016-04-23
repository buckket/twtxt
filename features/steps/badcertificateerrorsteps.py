from behave import *
import asyncio
import twtxt.models
import twtxt.twhttp
import twtxt.config
import aiohttp
from twtxt.cache import Cache


@given("a source <username> at <url> with a bad certificate")
def step_impl(context):
    context.ctx=twtxt.config.Config.discover()
    context.name="adiabatic"
    context.url="https://expired.badssl.com/"
    context.source=twtxt.models.Source(context.name,context.url)
@when("the goes to retreive tweets from the source")
def step_impl(context):
        cache=twtxt.cache.Cache.discover()
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            context.s=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,context.source,30,cache))

@then("an error message stating there is a bad certificate should be displayed")
def step_impl(context):
    assert(context.s==[])




@given("a source <username> at <url> with a valid certificate")
def step_impl(context):
    context.name="beyond"
    context.url="https://enotty.dk/beyond.txt"
    context.source=twtxt.models.Source(context.name,context.url)
@when("the program goes to retrieve tweets from that source")
def step_impl(context):
        cache=twtxt.cache.Cache.discover()
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            context.tweets=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,context.source,30,cache))
@then("a number of tweets greater than 0 should be retreived")
def step_impl(context):
    assert(len(context.tweets)>0)