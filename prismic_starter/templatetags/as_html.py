from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def as_html(object, url_resolver):
    return mark_safe(object.as_html(url_resolver))