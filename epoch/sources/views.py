from django.shortcuts import render
from .models import Source, Headline
from django.shortcuts import redirect
from django.contrib import messages  # import messages
from datetime import datetime, timedelta
from .filters import HeadlineFilter
from django.contrib.auth.decorators import login_required
from .forms import CustomSourceForm
from .parser import RSSParser
from .tasks import fetch_custom_rss_for_user


@login_required
def sources(request):
    current_user = request.user
    my_sources: list[Source] = Source.objects.all().filter(
        subscribers__in=[current_user.pk])
    users_timezone = current_user.userconfig.timezone
    if request.method == "POST":
        form = CustomSourceForm(request.POST)
        if form.is_valid():
            source_url = form.cleaned_data["custom_source"]
            fetch_custom_rss_for_user.delay(source_url, current_user.pk)
            messages.success(
                request, "Attempting to process RSS Feed. Please wait 5-10 minutes.")
            return redirect("sources")
        else:
            return render(request, "sources/sources.html", {"form": form, "sources": sources, "my_sources": my_sources, "users_timezone": users_timezone})
    else:
        form = CustomSourceForm()
        return render(request, "sources/sources.html", {"form": form, "my_sources": my_sources, "users_timezone": users_timezone})


@login_required
def community_sources(request):
    com_sources: list[Source] = Source.objects.filter(is_community=True)
    users_timezone = request.user.userconfig.timezone
    return render(request, "sources/community_sources.html", {"com_sources": com_sources, "users_timezone": users_timezone})


@login_required
def source_detail(request, source_id):
    users_timezone = request.user.userconfig.timezone
    requested_source = Source.objects.get(pk=source_id)
    sample_headlines = Headline.objects.all().filter(
        source=requested_source.pk)[:4]
    return render(request, "sources/source-detail.html", {"source": requested_source, "sample_headlines": sample_headlines, "users_timezone": users_timezone})


@login_required
def news(request):
    current_user = request.user
    users_timezone = current_user.userconfig.timezone
    users_subscribed_sources: list[Source] = Source.objects.all().filter(
        subscribers__in=[current_user.pk]).values_list("id", flat=True)
    qry = Headline.objects.all().filter(source_id__in=users_subscribed_sources)
    f = HeadlineFilter(request.GET, queryset=qry, request=request)
    return render(request, "sources/news.html", {"filter": f, "users_timezone": users_timezone})


@login_required
def news_detail(request, headline_id):
    users_timezone = request.user.userconfig.timezone
    requested_headline = Headline.objects.get(pk=headline_id)
    return render(request, "sources/news-detail.html", {"headline": requested_headline, "users_timezone": users_timezone})


@login_required
def add_source(request, source_id):
    current_user = request.user
    source_added: Source = Source.objects.get(pk=source_id)
    source_added.subscribers.add(current_user)
    messages.success(request, "Successfully added a new source.")
    return redirect(sources)


@login_required
def delete_source(request, source_id):
    current_user = request.user
    source_added: Source = Source.objects.get(pk=source_id)
    source_added.subscribers.remove(current_user)
    messages.info(request, "Successfully removed source.")
    return redirect(sources)
