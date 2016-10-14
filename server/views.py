# -*- coding: utf-8 -*-
from django.shortcuts import render
from quest.models import Settings

def handler400(request):
    return error(request)

def handler404(request):
    return error(request)

def handler500(request):
    return error(request)

def error(request):
    settings = Settings.getDict()
    settings['view'] = 'error'
    page_settings = {'title': 'Ошибка', 'description': ''}
    return render(request, 'error.html', {'settings': settings, 'page_settings': page_settings})
