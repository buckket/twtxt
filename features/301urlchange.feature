Feature: the program changse a source's url after getting a 301 error
  Scenario: A Url needs to be rerouted
    Given a source with a valid nickname and expired URL
    When program attempts to get tweets fromm remote source
    Then the Source's url will be changed to the new url
  Scenario: Source's url is still valid
    Given a source with a valid nickname and URL
    When users views tweets
    Then the source's url will still be unchanged
