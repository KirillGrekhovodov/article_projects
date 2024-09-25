from behave import fixture, use_fixture
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium.webdriver import Chrome
from django.test.runner import DiscoverRunner

from webapp.test.factory.article_factory import ArticleFactory
from webapp.test.factory.user_factory import UserFactory

from django.apps import apps

@fixture
def browser_chrome(context):
    context.browser = Chrome()
    yield context.browser
    context.browser.quit()


def before_all(context):
    use_fixture(browser_chrome, context)
    # context.fixtures = ["auth_dump.json", "dump.json"]
    live_server = StaticLiveServerTestCase()
    live_server.setUpClass()
    context.live_server_url = live_server.live_server_url
    context._live_server = live_server
    # call_command('loaddata', "auth_dump.json")
    # UserFactory.create(
    #     username="admin",
    #     password="admin",
    #     is_superuser=True,
    #     is_staff=True,
    # )
    # ArticleFactory.create_batch(5)

def after_scenario(context, scenario):
    for model in apps.get_models():
        model.objects.all().delete()