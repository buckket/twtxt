Feature: Error Messages for bad certificates
  Scenario: program tries to retrieve tweets from a source with a bad certificate
    Examples sourceswithexpiredSSLcertificates:
      | username | url |
      | adiabatic| https://expired.badssl.com/ |
      | beyond   | https://sha1-2017.badssl.com/ |
    Given a source <username> at <url> with a bad certificate
    When the goes to retreive tweets from the source
    Then an error message stating there is a bad certificate should be displayed



  Scenario: program tries to retrieve tweets from a source with a valid certificate
    Examples:
      | username | url |
      | adiabatic | https://www.frogorbits.com/twtxt.txt |
      | beyond | https://enotty.dk/beyond.txt |
    Given a source <username> at <url> with a valid certificate
    When the program goes to retrieve tweets from that source
    Then a number of tweets greater than 0 should be retreived
