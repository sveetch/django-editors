from django.core.exceptions import ValidationError

import pytest

from sandbox.demo.models import Article


def test_basic(db, tests_settings):
    """
    Basic model saving with required fields should not fail
    """
    article = Article(title="Bar")
    article.full_clean()
    article.save()

    url = "/{article_pk}/".format(
        article_pk=article.id,
    )

    assert 1 == Article.objects.filter(title="Bar").count()
    assert "Bar" == article.title
    assert url == article.get_absolute_url()


def test_required_fields(db):
    """
    Basic model validation with missing required files should fail
    """
    article = Article()

    with pytest.raises(ValidationError) as excinfo:
        article.full_clean()

    assert excinfo.value.message_dict == {
        "title": ["This field cannot be blank."],
    }
