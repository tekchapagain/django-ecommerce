from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, args):
    try:
        return value * args
    except(ValueError, TypeError):
        return 0