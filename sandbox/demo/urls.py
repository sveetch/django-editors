from django.urls import path

from .views import (
    ArticleIndexView,
    ArticleDetailView,
    EditorSampleView,
)


app_name = "demo"


urlpatterns = [
    path("", ArticleIndexView.as_view(), name="article-index"),
    path(
        "<int:article_pk>/",
        ArticleDetailView.as_view(),
        name="article-detail"
    ),
    path(
        "sample/<slug:editor_name>/",
        EditorSampleView.as_view(),
        name="editor-sample"
    ),
]
