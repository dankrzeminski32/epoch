from django.shortcuts import render
from .models import Source, Headline
from django.shortcuts import redirect


def sources(request):
    sources: list[Source] = Source.objects.all()
    return render(request, "sources/sources.html", {"sources": sources})


def news(request):
    headlines: list[Headline] = Headline.objects.all()
    return render(request, "sources/sources.html", {"sources": sources})


def add_source(request, source_id):
    current_user = request.user
    source_added: Source = Source.objects.get(pk=source_id)
    source_added.subscribers.add(current_user)
    return redirect(sources)
