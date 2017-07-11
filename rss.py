"""
This module works with rss-feed. The main function is 'check_for_game' that parse RSS-feed and return the game info.
"""
import feedparser
import re
from datetime import datetime, date


def clear_tags(raw_text):
    """
    This function returns text without html/xml tags
    :param raw_text: raw html/xml text
    :type raw_text: str
    :return: string-text without tags
    :rtype: str
    """
    pattern = re.compile('<.*?>')
    text = raw_text.replace('<br />', '\n')
    text = text.replace('&quot;', '"')
    text = re.sub(pattern, '', text)
    return text


def convert_date(text_date):
    """
    This function convert date from text format to datetime-format
    :param text_date: date in text-format
    :type text_date: str
    :return: date in datetime-format
    :rtype: datetime
    """
    days = {'январ': 1,
            'феврал': 2,
            'март': 3,
            'апрел': 4,
            'ма': 5,
            'июн': 6,
            'июл': 7,
            'август': 8,
            'сентябр': 9,
            'октябр': 10,
            'ноябр': 11,
            'декабр': 12}
    pattern = re.compile('(.*?), ([\d]{2}) (.*?), ([\d]{2})-([\d]{2})')
    match = pattern.search(text_date)
    if match:
        day = int(match.group(2))
        month = match.group(3)
        hours = int(match.group(4))
        mins = int(match.group(5))
        year = date.today().year
        for key in days:
            if key in month:
                month = days[key]
                event_date = datetime(year, month, day, hours, mins)
                return event_date
    else:
        return False


def get_id(url):
    """
    This function pop postID from text-url
    :param url: url in text-format
    :type url: str
    :return: postID
    :rtype: int
    """
    pattern = re.compile('com\/(.*?).html')
    match = pattern.search(url)
    if match:
        post_id = int(match.group(1))
        return post_id


def check_for_game(feed_url, number=0):
    """
    This function parse the rss-feed and return the dict with game info.
    :param feed_url: URL of RSS-feed in string-format
    :param number: (Optional) number of items to parse. Default = 1.
    :type feed_url: str
    :type number: int
    :return: Dict with game info ("name", "date", "text", "id").
    :rtype: dict
    """
    game = {"name": '',
            "date": '',
            "text": '',
            "id": ''}
    pattern_what = re.compile('Что: (.*).')
    pattern_when = re.compile('Когда: (.*).')
    feed_data = feedparser.parse(feed_url)
    items = feed_data["items"]
    item_body = items[number].summary_detail.value
    item_text = clear_tags(item_body)
    match_what = pattern_what.search(item_text)
    if match_what:
        game["name"] = match_what.group(1)
        game["name"] = game["name"][0].upper() + game["name"][1:]
    match_when = pattern_when.search(item_text)
    if match_when:
        game["date"] = convert_date(match_when.group(1))
    if get_id(items[number]['link']):
        game["id"] = get_id(items[number]['link'])
    if game["name"] and game["date"] and game["id"]:
        game["text"] = item_text
        return game
