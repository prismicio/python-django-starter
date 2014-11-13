from django import template

register = template.Library()

context_name = "context"


@register.simple_tag(takes_context=True)
def as_html(context, object):
    return object.as_html(context[context_name]["link_resolver"])


@register.simple_tag(takes_context=True)
def get_html(context, object, field):
    return object.get_html(field, context[context_name]["link_resolver"])


@register.simple_tag
def get_text(document, field):
    return document.get_text(field)


@register.simple_tag
def get_number(document, field, format=None):
    number = document.get_number(field).value
    if format:
        return format % number
    else:
        return number


@register.simple_tag
def get_image(document, field, view="main"):
    image = document.get_image(field, view)
    return image.url if image else None


@register.simple_tag(takes_context=True)
def experiments(context):
    google_id = context[context_name]["google_id"]
    if google_id is None:
        return ""
    else:
        return """<script src="//www.google-analytics.com/cx/api.js?experiment=@googleId"></script>
<script>prismic.startExperiment("@googleId", cxApi);</script>"""
