from django.shortcuts import render
from .models import Source, Headline
from django.shortcuts import redirect
from django.contrib import messages  # import messages
from datetime import datetime, timedelta
from .filters import HeadlineFilter


def sources(request):
    current_user = request.user
    sources: list[Source] = Source.objects.all()
    my_sources: list[Source] = Source.objects.all().filter(
        subscribers__in=[current_user.pk])
    return render(request, "sources/sources.html", {"sources": sources, "my_sources": my_sources})


def news(request):
    current_user = request.user
    users_subscribed_sources: list[Source] = Source.objects.all().filter(
        subscribers__in=[current_user.pk]).values_list("id", flat=True)
    qry = Headline.objects.all().filter(source_id__in=users_subscribed_sources)
    f = HeadlineFilter(request.GET, queryset=qry, request=request)
    print(f.qs.query)

    return render(request, "sources/news.html", {"filter": f})


def news_detail(request, headline_id):
    requested_headline = Headline.objects.get(pk=headline_id)
    print(requested_headline)
    return render(request, "sources/news-detail.html", {"headline": requested_headline})


def add_source(request, source_id):
    current_user = request.user
    source_added: Source = Source.objects.get(pk=source_id)
    source_added.subscribers.add(current_user)
    messages.success(request, "Successfully added a new source.")
    return redirect(sources)


def delete_source(request, source_id):
    current_user = request.user
    source_added: Source = Source.objects.get(pk=source_id)
    source_added.subscribers.remove(current_user)
    messages.info(request, "Successfully removed source.")
    return redirect(sources)
