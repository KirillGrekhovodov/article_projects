from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from webapp.models import Article
from webapp.test.factory.article_factory import ArticleFactory
from webapp.test.factory.user_factory import UserFactory

User = get_user_model()


class TestArticlesViews(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(password='password')

    @classmethod
    def tearDownClass(cls):
        pass


    def test_articles_list(self):
        ArticleFactory.create(title="Test Article")
        response = self.client.get("/articles/")
        self.assertTemplateUsed(response, 'articles/index.html')
        self.assertContains(response, 'Test Article')


    def test_article_create(self):
        data = {
            "title": "Test Article",
            "content": "Test Content",
        }
        self.client.login(username=self.user.username, password="password")
        response = self.client.post("/create/", data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Article.objects.count(), 1)
        new_article = Article.objects.first()
        self.assertEqual(new_article.title, data["title"])
        self.assertEqual(new_article.author, self.user)

    def test_article_create_no_content(self):
        data = {
            "title": "Test Article",
        }
        self.client.login(username=self.user.username, password="password")
        response = self.client.post("/create/", data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Article.objects.count(), 0)

    def test_article_update_success_for_author(self):
        article = ArticleFactory.create(author=self.user)
        data = {
            "title": "Update Article",
            "content": "Update Content",
        }
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(reverse("webapp:update_article", kwargs={"pk": article.pk}), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        article.refresh_from_db()
        self.assertEqual(article.title, data["title"])
        self.assertEqual(article.content, data["content"])

    def test_article_update_success_for_admin(self):
        admin = UserFactory.create(password="password")
        admin.user_permissions.add(Permission.objects.get(codename="change_article"))
        article = ArticleFactory.create()
        data = {
            "title": "Update Article",
            "content": "Update Content",
        }
        self.client.login(username=admin.username, password="password")
        response = self.client.post(reverse("webapp:update_article", kwargs={"pk": article.pk}), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        article.refresh_from_db()
        self.assertEqual(article.title, data["title"])
        self.assertEqual(article.content, data["content"])


    def test_article_update_failed_not_permissions(self):
        user = UserFactory.create(password="password")
        article = ArticleFactory.create(title="Test Article")
        data = {}
        self.client.login(username=user.username, password="password")
        response = self.client.post(reverse("webapp:update_article", kwargs={"pk": article.pk}), data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        article.refresh_from_db()
        self.assertEqual("Test Article", article.title)
        # self.assertTemplateUsed(response, 'webapp/templates/update_article.html')


    def test_article_update_failed_no_authenticated(self):
        article = ArticleFactory.create(title="Test Article")
        data = {}
        url = reverse("webapp:update_article", kwargs={"pk": article.pk})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f'/accounts/login/?next={url}')
        article.refresh_from_db()
        self.assertEqual("Test Article", article.title)

