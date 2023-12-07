from django.core.management.base import BaseCommand, CommandError
from sources.parser import RSSParser


class Command(BaseCommand):
    help = "Populates an initial seed of RSS Feeds"

    def handle(self, *args, **options):

        parser = RSSParser()
        f = open("./community_rss_feeds.txt", "r").read().splitlines()
        for url in f:
            self.stdout.write(
                self.style.NOTICE(
                    'Attempting to retrieve feed for %s' % url)
            )
            source = parser.get_source(url)
            if source:
                source.is_community = True
                source.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully seeded source - %s' % source.link)
                )
                headlines = parser.get_headlines_for_source(source)
                if headlines:
                    for headline in headlines:
                        headline.save()
            else:
                self.stdout.write(
                    self.style.ERROR(
                        'Failed to seed source')
                )
