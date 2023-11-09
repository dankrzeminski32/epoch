from django.shortcuts import render
from .models import Source, Headline
from django.shortcuts import redirect


def sources(request):
    sources: list[Source] = Source.objects.all()
    return render(request, "sources/sources.html", {"sources": sources})


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


def add_source(request, source_id):
    current_user = request.user
    source_added: Source = Source.objects.get(pk=source_id)
    source_added.subscribers.add(current_user)
    return redirect(sources)
