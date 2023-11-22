from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import pytz


class Source(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, default="")
    description = models.CharField(max_length=255, blank=True, default="")
    published = models.DateTimeField(null=True, blank=True)
    img_link = models.CharField(max_length=255, blank=True, default="")
    is_community = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(get_user_model())

    def __str__(self):
        return f'Source({self.title}, {self.link}, {self.description}, {self.published})'

    def __repr__(self):
        return f'Source({self.title}, {self.link}, {self.description}, {self.published})'

    @property
    def number_of_subscribers(self):
        subs_count = self.subscribers.all().count()
        return subs_count

    @property
    def number_of_headlines(self):
        return Headline.objects.all().filter(source=self.pk).count()


class Headline(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    published = models.DateTimeField()
    img = models.CharField(max_length=255, blank=True, null=True, default="")
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    @property
    def is_from_current_week(self):
        now = datetime.now(tz=pytz.UTC)
        monday = now - timedelta(days=now.weekday())
        monday_start_of_day = monday.replace(hour=0, minute=0, second=0)
        return self.published > monday_start_of_day
