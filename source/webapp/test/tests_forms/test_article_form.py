from django.contrib.auth import get_user_model
from django.test import TestCase

from webapp.forms import ArticleForm


User = get_user_model()


class TestArticlesForm(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = ArticleForm()

    @classmethod
    def tearDownClass(cls):
        pass


    def test_article_create_no_content_failed(self):
        data = {
            "title": "Test Article",
        }
        form = ArticleForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertListEqual(form.errors["content"], ["This field is required."])
