from django import template

# Django is weird and does not allow for underscores in template tags
# As we need _source and _id in templates, we need to create a custom tag
# See: https://stackoverflow.com/questions/48038126/variables-and-attributes-may-not-begin-with-underscores-in-django-template

register = template.Library()

@register.simple_tag
def underscoreTag(obj, attribute):
    obj = dict(obj)
    return obj.get(attribute)