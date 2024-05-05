from django import template

# Django is weird and does not allow for underscores in template tags
# As we need _source and _id in templates, we need to do some workarounds
# See: https://stackoverflow.com/questions/13693888/accessing-dict-elements-with-leading-underscores-in-django-templates

register = template.Library()

@register.filter(name='get')
def get(d, k):
    return d.get(k, None)
