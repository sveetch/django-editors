from django_editors.utils.tests import html_pyquery

from sandbox.demo.factories import ArticleFactory


def test_article_detail_404(db, client):
    """
    Try to reach unexisting article should return a 404 response.
    """
    response = client.get("/42/", follow=True)

    assert response.status_code == 404


def test_article_detail_content(db, client):
    """
    Article content should be displayed correctly.
    """
    article = ArticleFactory()

    response = client.get(article.get_absolute_url())
    assert response.status_code == 200

    dom = html_pyquery(response)
    article_title = dom.find(".article-detail .title")
    article_content = dom.find(".article-detail .content")

    assert article_title.text() == article.title
    # Prevent 'text()' method to remove white spaces because content may contains some
    # line breaks
    assert article_content.text(squash_space=False) == article.content
