import django_filters
from sources.models import Headline
from django_filters import DateFromToRangeFilter, ModelChoiceFilter, ChoiceFilter, CharFilter
from django_filters.widgets import RangeWidget
from .models import Source
from django import forms


def get_users_sources(request):
    print(request)
    if request is None:
        return Source.objects.none()
    current_user = request.user
    return Source.objects.all().filter(
        subscribers__in=[current_user.pk]).values_list("id", "title")


class HeadlineFilter(django_filters.FilterSet):
    published = DateFromToRangeFilter(label="Date  ",
                                      widget=RangeWidget(
                                          attrs={'class': 'form-control w-50 mx-1',
                                                 'placeholder': 'dd/mm/yyyy', 'type':  'date'})
                                      )
    source_id = ChoiceFilter(
        empty_label="Select a Source ",
        widget=forms.Select(attrs={'class': 'form-control w-75'})
    )
    title = CharFilter(label="Title ", lookup_expr="contains", widget=forms.TextInput(
        attrs={'class': 'form-control w-75', 'placeholder': 'Big Tech, S&P500, etc.'}))

    def __init__(self, *args, **kwargs):
        super(HeadlineFilter, self).__init__(*args, **kwargs)
        self.filters["source_id"].extra["choices"] = get_users_sources(
            request=self.request)

    class Meta:
        model = Headline
        fields = ['title', 'published', 'source_id']
