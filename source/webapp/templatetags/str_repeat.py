from django import template

register = template.Library()


@register.filter
def repeat(value, arg):
    return value * arg


@register.filter
def test_func(value):
    return value
