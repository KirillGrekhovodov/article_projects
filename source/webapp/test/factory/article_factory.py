import factory

from webapp.models import Article
from webapp.models.article import statuses
from webapp.test.factory.user_factory import UserFactory


class ArticleFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Article {n}")
    content = factory.Faker("paragraph", nb_sentences=10)
    author = factory.SubFactory(UserFactory)
    status = factory.Iterator([s[0] for s in statuses])


    class Meta:
        model = Article