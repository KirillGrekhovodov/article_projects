from time import sleep

from behave import given, when, then
from behave_django.decorators import fixtures
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from webapp.models import Article

User = get_user_model()


@fixtures("auth_dump.json")
@fixtures("dump.json")
@given('Я открыл страницу "Входа"')
def step_impl(context):
    print(User.objects.all())
    context.browser.get(context.live_server_url + '/accounts/login/')


@when('Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element(By.NAME, name).send_keys(text)


@when('Я отправляю форму')
def submit_form(context):
    form = context.browser.find_element(By.CSS_SELECTOR, 'form')
    form.submit()


@then('Я должен быть на главной странице')
def should_be_at_main(context):
    sleep(5)
    assert context.browser.current_url == context.live_server_url + '/articles/'


@then("Я должен быть на странице входа")
def should_be_at_login(context):
    assert context.browser.current_url == context.live_server_url + '/accounts/login/'


@then('Я должен видеть сообщение об ошибке с текстом "{text}"')
def see_error_with_text(context, text):
    print(User.objects.all(), "empty")
    error = context.browser.find_element(By.CLASS_NAME, 'text-danger')
    assert error.text == text


@then('Я должен видеть заголовок "{text}"')
def see_h1_with_text(context, text):
    h1 = context.browser.find_element(By.CSS_SELECTOR, '.container>h1')
    assert h1.text == text
