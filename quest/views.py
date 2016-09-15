from django.shortcuts import render
from django.template import loader
from .models import Quest
from .models import QuestImage
from .models import GoogleDriveDoc
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Settings
from .models import Page
from .models import Discount
from django.urls import reverse
import random


def index(request):
    quests = Quest.objects.order_by('in_construct', 'order')
    discounts = Discount.objects.order_by('order')
    settings = Settings.getDict()
    settings['view'] = 'index'
    template = loader.get_template('quest/index2.html')
    context = {'quests': quests, 'settings': settings, 'discounts': discounts}
    return HttpResponse(template.render(context, request))

def quest(request, quest_id):
    template = loader.get_template('quest/quest2.html')
    settings = Settings.getDict()
    settings['view'] = 'quest'
    quest = Quest.objects.get(id=quest_id)
    context = {'quest': quest, 'settings': settings}
    return HttpResponse(template.render(context, request))

def quest_get_remain_imgs(request):
    quest_id = request.GET.get('quest_id')
    quest = Quest.objects.get(id=quest_id)
    imgs = quest.questimage_set.filter(order__gt=1, type='img')
    return JsonResponse({i.id: {'url': i.image.url, 'order': i.order} for i in imgs})

def google_doc_get_random_player_images(request):
    count = request.GET.get('count')
    imgs = GoogleDriveDoc.objects.filter(type='img-p').order_by('?')[:count].values_list('id', flat=True)
    imgs = [i.encode('UTF-8') for i in imgs]
    return JsonResponse({'items': imgs})

def gifts(request):
    settings = Settings.getDict()
    settings['view'] = 'gifts'
    page = Page.objects.get(name='gifts')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    page_imgs = {pi['name']: pi['image'] for pi in page.pageimage_set.values()}
    template = loader.get_template('quest/gifts.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'imgs': page_imgs}
    return HttpResponse(template.render(context, request))

def amauters(request):
    settings = Settings.getDict()
    settings['view'] = 'amauters'
    template = loader.get_template('quest/amauters.html')
    page = Page.objects.get(name='amauters')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    page_imgs = {pi['name']: pi['image'] for pi in page.pageimage_set.values()}
    imgs = [{'image': i['image'], 'order': i['order'], 'title': i['quest__name'], 'url': reverse('quest', args=[i['quest']])} for i in
            QuestImage.objects.filter(type='ama').values('quest__name', 'quest', 'image', 'order')]
    random.shuffle(imgs)
    imgs2 = list(imgs)
    random.shuffle(imgs2)
    imgs3 = list(imgs)
    random.shuffle(imgs3)

    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'quest_imgs': imgs,
               'page_imgs': page_imgs,
               'quest_imgs2': imgs2,
               'quest_imgs3': imgs3, 'carousel_options': {'certainHeight': False}}
    return HttpResponse(template.render(context, request))

def birthday(request):
    settings = Settings.getDict()
    settings['view'] = 'birthday'
    template = loader.get_template('quest/birthday.html')
    page = Page.objects.get(name='birthday')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = [{'image': i['image'], 'order': i['order'], 'title': i['name']} for i in page.pageimage_set.values('image', 'name', 'order')]
    context = {'settings': settings, 'blocks': page_text_blocks, 'imgs': imgs}
    return HttpResponse(template.render(context, request))

def shedule(request):
    settings = Settings.getDict()
    quests = Quest.objects.order_by('in_construct', 'order')
    discounts = Discount.objects.order_by('order')
    settings['view'] = 'shedule'
    page = Page.objects.get(name='shedule')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    template = loader.get_template('quest/shedule.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'quests': quests, 'discounts': discounts}
    return HttpResponse(template.render(context, request))

def animators(request):
    settings = Settings.getDict()
    settings['view'] = 'animators'
    page = Page.objects.get(name='animators')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    template = loader.get_template('quest/animators.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks}
    return HttpResponse(template.render(context, request))

def contacts(request):
    settings = Settings.getDict()
    settings['view'] = 'contacts'
    page = Page.objects.get(name='contacts')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    template = loader.get_template('quest/contacts.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks}
    return HttpResponse(template.render(context, request))
