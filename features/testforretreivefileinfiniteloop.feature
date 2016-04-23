Feature: twhttp bug fix
  Scenario: twhttp gets tweets from a remote source
  Examples: TweetSources
    | username    | url                                                |
    | kas         | https://enotty.dk/twtxt.txt                        |
    | xena        | https://xena.greedo.xeserv.us/files/xena.txt       |
    | texttheater | https://texttheater.net/twtxt                      |
    | mdom        | https://mdom.github.io/twtxt.txt                   |
    | reednj      | http://reednj.com/reednj.twtxt.txt                 |
    | myles       | http://twtxt.mylesb.ca/                            |
    | dracoblue   |https://dracoblue.net/twtxt.txt                     |
    | david       |https://post.aldebaran.uberspace.de/twtxt/david.txt |
    Given a source <username> at <url> is provided
    When the program tries to retrieve tweets from a remote source
    Then a list of tweets with a length greater than 0 should be returned

