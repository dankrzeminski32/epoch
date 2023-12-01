from .parser import RSSParser
from celery import shared_task
from .models import Source
from django.contrib.auth.models import User


@shared_task()
def fetch_custom_rss_for_user(url: str, user_pk: int):
    print(url)
    print(user_pk)
    rss_parser = RSSParser()
    new_source: Source = rss_parser.get_source(url)
    if new_source:
        new_source.save()
        user_that_submitted_request = User.objects.get(id=user_pk)
        new_source.subscribers.add(user_that_submitted_request)
        headlines = rss_parser.get_headlines_for_source(new_source)
        for headline in headlines:
            headline.save()
