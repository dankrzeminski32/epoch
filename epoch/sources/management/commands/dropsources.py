from django.core.management.base import BaseCommand
from sources.models import Source


class Command(BaseCommand):
    help = "Populates an initial seed of RSS Feeds"

    def handle(self, *args, **options):
        Source.objects.all().delete()
