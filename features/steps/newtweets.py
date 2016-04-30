from behave import *

import twtxt.helper
import twtxt.cli
import twtxt.config
import twtxt.models
import twtxt.cache
import twtxt.mentions

@given("there are no new tweets")
def step_impl(context):
	lastViewed = context.ctx.obj["conf"].get_last_viewed()
	if get_new_tweets(context.tweet, lastViewed) != True:
		assert(True)
	else:
		assert(False)
	
@when("the option -nt is used")
def step_impl(context):
	#assumed
	assert(True)
	
@then("show nothing in the timeline")
def step_impl(context):
	assert(len(context.tweets) <= 0)
	
#-----------------------------------------------------------

@given("there are new tweets that are unread")
def step_impl(context):
	context.ctx=twtxt.config.Config.discover()
	timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	tweet(context.ctx, timeNow, "twtxt.txt", "New tweet from behave")
	
	lastViewed = context.ctx.obj["conf"].get_last_viewed()
	if get_new_tweets(context.tweet, lastViewed) != False:
		assert(True)
	else:
		assert(False)
	
#Already defined in previous test so no need to redefine!
	
@then("show the new tweets in the timeline")
def step_impl(context):
	assert(len(context.tweets) > 0)