from django import template
from urllib.parse import urlencode

register = template.Library()


# Custom template tag to pass search parameters to our pagination
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()


# Custom template tag to return the model name of an object
@register.filter
def to_class_name(value):
    return value.__class__.__name__
