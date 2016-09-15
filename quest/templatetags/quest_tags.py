from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('quest/carousel2.html')
def quest_carousel(id, items, options = {'certainHeight': False}):
    return {'id': id, 'items': items, 'options': options}