Feature: Limiting timeline by only showing unread tweets from last read of timeline

	Scenario: No new tweets to show
		Given: there are no new tweets
		When: the option -nt is used
		Then: show nothing in the timeline
		
	Scenario: New tweets are available
		Given: there are new tweets that are unread
		When: the option -nt is used
		Then: show the new tweets in the timeline