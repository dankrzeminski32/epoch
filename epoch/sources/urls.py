from django.urls import path
from . import views

urlpatterns = [
    path("", views.sources, name="sources"),
    path("community", views.community_sources, name="community-sources"),
    path("add/<int:source_id>", views.add_source, name="add-source"),
    path("delete/<int:source_id>", views.delete_source, name="delete-source"),
    path("detail/<int:source_id>",
         views.source_detail, name="source-detail")
]
