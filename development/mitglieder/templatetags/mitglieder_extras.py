from django import template

register = template.Library()

@register.filter
def amtszeit_ende_isnull(value):
    if value is None:
        return True
    return False
