from django.utils import timezone

import factory

from ..models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of an Article.
    """
    title = factory.Faker("text", max_nb_chars=50)
    content = factory.Faker("text", max_nb_chars=150)

    class Meta:
        model = Article

    @factory.lazy_attribute
    def publish_start(self):
        """
        Return current date.

        Returns:
            datetime.datetime: Current time.
        """
        return timezone.now()
