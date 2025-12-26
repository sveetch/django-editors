from sandbox.demo.factories import ArticleFactory


def test_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    article = ArticleFactory(title="foo")

    assert article.title == "foo"
