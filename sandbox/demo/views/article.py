from django.views.generic import DetailView, ListView

from ..models import Article


class ArticleIndexView(ListView):
    """
    List of articles
    """
    model = Article
    queryset = Article.objects.order_by("publish_start")
    template_name = "demo/article_index.html"
    paginate_by = 5


class ArticleDetailView(DetailView):
    """
    Article detail
    """
    pk_url_kwarg = "article_pk"
    template_name = "demo/article_detail.html"
    context_object_name = "article_object"

    def get_queryset(self):
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
