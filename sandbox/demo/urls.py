from django.urls import path

from .views import (
    ArticleIndexView,
    ArticleDetailView,
)


app_name = "demo"


urlpatterns = [
    path("", ArticleIndexView.as_view(), name="article-index"),
    path(
        "<int:article_pk>/",
        ArticleDetailView.as_view(),
        name="article-detail"
    ),
]
