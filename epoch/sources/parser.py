import feedparser
from datetime import datetime
from .models import Source, Headline
from time import mktime
from datetime import datetime
from io import StringIO
from html.parser import HTMLParser


class HTMLTagStripper(HTMLParser):
    """Strips html tags from text"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


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

    def _strip_html_tags(self, html):
        tag_stripper = HTMLTagStripper()
        tag_stripper.feed(html)
        return tag_stripper.get_data()

    def get_source(self, feed_url) -> Source:
        """returns details of an RSS source if the link is valid, otherwise returns None"""
        try:
            raw_response_data = self._parse(feed_url)
            new_source = Source(link=feed_url)
            if hasattr(raw_response_data.feed, "image"):
                new_source.img_link = raw_response_data.feed.image["href"]
            new_source.title = raw_response_data.feed.get("title", "No Title")
            new_source.description = self._strip_html_tags(raw_response_data.feed.get(
                "description", "No Description"))
            if "updated_parsed" in raw_response_data.feed:
                new_source.published = datetime.fromtimestamp(
                    mktime(raw_response_data.feed.updated_parsed))
            return new_source
        except InvalidRSSURL:
            return None

    def get_headlines_for_source(self, feed_url) -> list[Headline]:
        """returns headlines for an RSS source"""
        try:
            src = Source.objects.all().filter(link=feed_url)[0]
            raw_response_data = self._parse(feed_url)
            headlines = []
            for entry in raw_response_data.entries:
                pub_date = datetime.fromtimestamp(
                    mktime(entry.updated_parsed))
                new_headline = Headline(
                    title=entry.title,
                    description=self._strip_html_tags(entry.description),
                    published=pub_date,
                    source_id=src.pk
                )
                headlines.append(new_headline)
            return headlines
        except InvalidRSSURL:
            return None

        except InvalidRSSURL:
            return None


class InvalidRSSURL(Exception):
    pass
