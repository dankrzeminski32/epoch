import feedparser
from datetime import datetime
from .models import Source, Headline
from time import mktime
from datetime import datetime
from io import StringIO
from html.parser import HTMLParser
from bs4 import BeautifulSoup as BS
import pytz


class RSSParser:
    """Wrapper class to parse rss feeds into epoch models"""

    def __init__(self):
        self._parser = feedparser

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
                    mktime(raw_response_data.feed.updated_parsed), tz=pytz.UTC)
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
                    mktime(entry.updated_parsed), tz=pytz.UTC)
                new_headline = Headline(
                    title=entry.title,
                    description=self._strip_html_tags(entry.description),
                    published=pub_date,
                    source_id=src.pk,
                    link=entry.get("link", ""),
                    img=self._get_entry_image(entry),
                )
                headlines.append(new_headline)
            return headlines
        except InvalidRSSURL:
            return None

    def _parse(self, feed_url):
        data = self._parser.parse(feed_url)
        if len(data.feed) == 0:
            raise InvalidRSSURL(
                "The RSS url gave an invalid response.")
        return data

    def _get_entry_image(self, entry) -> str | None:
        if entry.get("media_content", None):
            content = entry.media_content[0].get("url", None)
            if content:
                return content
        if entry.get("media_thumbnail", None):
            thumbnail = entry.media_thumbnail[0].get("url", None)
            if thumbnail:
                return thumbnail

        if entry.get("content", None):
            for item in entry.content:
                if item["type"] == "text/html":
                    return self._get_img_src(item["value"])
        return None

    def _strip_html_tags(self, html) -> str:
        tag_stripper = HTMLTagStripper()
        tag_stripper.feed(html)
        return tag_stripper.get_data()

    def _get_img_src(cls, html) -> str:
        soup = BS(html, features="html.parser")
        img_tag = soup.find('img')
        if img_tag:
            return img_tag['src']
        return None


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


class InvalidRSSURL(Exception):
    pass
