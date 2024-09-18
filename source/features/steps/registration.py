from behave import given
from django.contrib.auth import get_user_model

User = get_user_model()


@given('Я открыл страницу "Регистрации"')
def open_registration_page(context):
    User.objects.create_user(username="behave", password='correcthorsebatterystaple')
    print(User.objects.all())
    context.browser.get(context.live_server_url + '/accounts/register/')
