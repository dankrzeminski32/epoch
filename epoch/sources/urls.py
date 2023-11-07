from django.urls import path
from . import views

urlpatterns = [
    path("", views.sources, name="sources"),
    path("add/<int:source_id>", views.add_source, name="add-source"),
]
