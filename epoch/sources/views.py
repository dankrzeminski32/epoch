from django.shortcuts import render
from .models import Source


def sources(request):
    sources: list[Source] = Source.objects.all()
    return render(request, "sources/sources.html", {"sources": sources})
