# -*- coding: utf-8 -*-
from django.template import loader
from django.http import HttpResponse
from quest.models import Settings


def error(request):
    settings = Settings.getDict()
    settings['view'] = 'error'
    template = loader.get_template('404.html')
    context = {'settings': settings}
    return HttpResponse(template.render(context, request))