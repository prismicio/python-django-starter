from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def as_html(object, prismic_context):
    return mark_safe(object.as_html(prismic_context["link_resolver"]))