# -*- coding: utf-8 -*-
from django.shortcuts import render
from quest.models import Settings

def handler400(request):
    return error(request, 400)

def handler403(request):
    return error(request, 403)

def handler404(request):
    return error(request, 404)

def handler500(request):
    return error(request, 500)

def error(request, status):
    settings = Settings.getDict()
    settings['view'] = 'error'
    page_settings = {'title': 'Ошибка', 'description': ''}
    return render(request, 'error.html', {'settings': settings, 'page_settings': page_settings}, status=status)
