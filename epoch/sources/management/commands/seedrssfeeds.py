from django.core.management.base import BaseCommand, CommandError
from sources.parser import RSSParser


class Command(BaseCommand):
    help = "Populates an initial seed of RSS Feeds"

    def handle(self, *args, **options):

        parser = RSSParser()
        f = open("./community_rss_feeds.txt", "r")
        for url in f:
            source = parser.get_source(url)
            if source:
                print(source)
                source.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully seeded source')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        'Failed to seed source')
                )
