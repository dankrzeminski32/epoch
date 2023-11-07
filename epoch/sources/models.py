from django.db import models
from django.contrib.auth import get_user_model


class Source(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, default="")
    description = models.CharField(max_length=255, blank=True, default="")
    published = models.DateTimeField(null=True, blank=True)
    subscribers = models.ManyToManyField(get_user_model())

    def __str__(self):
        return f'Source({self.title}, {self.link}, {self.description}, {self.published})'

    def __repr__(self):
        return f'Source({self.title}, {self.link}, {self.description}, {self.published})'


class Headline(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    published = models.DateTimeField()
    img = models.CharField(max_length=255)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
