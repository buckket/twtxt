from functools import partial

from twtxt.mentions import format_mentions


def mock_mention_format(name, url, expected_name, expected_url):
    assert name == expected_name
    assert url == expected_url
    if name:
        return '@' + name
    else:
        return name


def test_format_mentions():
    texts = {'No Mention': 'No Mention',
             '@<SomeName http://some.url/twtxt.txt>': ('SomeName', 'http://some.url/twtxt.txt'),
             '@<Some>Shitty<Name http://some.url/twtxt.txt>': ('Some>Shitty<Name', 'http://some.url/twtxt.txt'),
             '@<http://some.url/twtxt.txt>': (None, 'http://some.url/twtxt.txt'),
             '@<SomeName>': '@<SomeName>',
             '@SomeName': '@SomeName'}
    for input, expected in texts.items():
        if isinstance(expected, tuple):
            format_mentions(input, partial(mock_mention_format, expected_name=expected[0], expected_url=expected[1]))
        else:
            assert expected == format_mentions(input,
                                               partial(mock_mention_format, expected_name=None, expected_url=None))


def test_format_multi_mentions():
    text = '@<SomeName http://url> and another @<AnotherName http://another/url> end'
    mentions = (('SomeName', 'http://url'),
                ('AnotherName', 'http://another/url'))

    def mock_multi_mention_format(name, url):
        return '@' + name

    format_mentions(text, mock_multi_mention_format)


def test_format_multi_mentions_incomplete():
    text = '@<http://url> and another @<AnotherName http://another/url> end'
    mentions = ((None, 'http://url'),
                ('AnotherName', 'http://another/url'))

    def mock_multi_mention_format(name, url):
        if name:
            return '@' + name
        else:
            return '@' + url

    format_mentions(text, mock_multi_mention_format)

    text = '@<SomeName http://url> and another @<http://another/url> end'
    mentions = (('SomeName', 'http://url'),
                (None, 'http://another/url'))
