from django.shortcuts import render
from .models import Source, Headline
from django.shortcuts import redirect
from django.contrib import messages  # import messages


def sources(request):
    current_user = request.user
    sources: list[Source] = Source.objects.all()
    my_sources: list[Source] = Source.objects.all().filter(
        subscribers__in=[current_user.pk])
    return render(request, "sources/sources.html", {"sources": sources, "my_sources": my_sources})


def news(request):
    current_user = request.user
    users_subscribed_sources: list[Source] = Source.objects.all().filter(
        subscribers__in=[current_user.pk])
    headlines: list[Headline] = []
    for source in users_subscribed_sources:
        qry = list(Headline.objects.all().filter(source=source.pk))
        headlines.append(qry)

    headlines = ([item for items in headlines for item in items])

    print(headlines)
    return render(request, "sources/news.html", {"headlines": headlines})


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
