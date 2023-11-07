import feedparser
from datetime import datetime
from .models import Source, Headline


class RSSParser:
    """Wrapper class to parse rss feeds into epoch models"""

    def __init__(self):
        self._parser = feedparser

    def _parse(self, feed_url):
        data = self._parser.parse(feed_url)
        if len(data.feed) == 0:
            raise InvalidRSSURL(
                "The RSS url gave an invalid response.")
        return data

    def _rss_date_to_datetime(self, date_str):
        datetime_object = datetime.strptime(
            date_str, '%a, %d %b %y %X %z')
        return datetime_object

    def get_source(self, feed_url) -> Source:
        """returns details of an RSS source if the link is valid, otherwise returns None"""
        try:
            raw_response_data = self._parse(feed_url)
            new_source = Source(link=feed_url)
            new_source.title = raw_response_data.feed.get("title", "")
            new_source.description = raw_response_data.feed.get(
                "description", "")
            # published_date = raw_response_data.feed.get("published")
            # if published_date:
            #    new_source.published = self._rss_date_to_datetime(
            #        published_date)
            return new_source
        except InvalidRSSURL:
            return None

    def get_headlines_for_source(self, feed_url) -> list[Headline]:
        try:
            raw_response_data = self._parse(feed_url)

        except InvalidRSSURL:
            return None


class InvalidRSSURL(Exception):
    pass
