# -*- coding: utf-8 -*-
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
from .models import Banner
from .models import *
from django.urls import reverse
import random
from django.http import Http404
import json

def index(request):
    quests = Quest.objects.order_by('in_construct', 'order')
    top_banner = Banner.objects.filter(type='top').order_by('order')
    discounts = Discount.objects.order_by('order')
    page = Page.objects.get(name='index')
    settings = Settings.getDict()
    settings['view'] = 'index'
    template = loader.get_template('quest/index2.html')
    context = {'quests': quests, 'settings': settings, 'discounts': discounts, 'page_settings': page, 'top_banner': top_banner}
    return HttpResponse(template.render(context, request))

def quest(request, quest_id):
    template = loader.get_template('quest/quest2.html')
    settings = Settings.getDict()
    settings['view'] = 'quest'
    try:
        quest = Quest.objects.get(id=quest_id)
    except Exception as ex:
        raise Http404()
    page_settings = {'title': quest.seo_title, 'description': quest.seo_description}
    context = {'quest': quest, 'settings': settings, 'page_settings': page_settings}
    return HttpResponse(template.render(context, request))

def quest_rewrite(request, quest_name):
    template = loader.get_template('quest/quest2.html')
    settings = Settings.getDict()
    settings['view'] = 'quest'
    try:
        quest = Quest.objects.get(seo_url=quest_name)
    except Exception as ex:
        raise Http404()
    page_settings = {'title': quest.seo_title, 'description': quest.seo_description}
    context = {'quest': quest, 'settings': settings, 'page_settings': page_settings}
    return HttpResponse(template.render(context, request))

def show_rewrite(request, show_name):
    template = loader.get_template('quest/show.html')
    settings = Settings.getDict()
    settings['view'] = 'show'
    try:
        show = Show.objects.get(seo_url=show_name)
    except Exception as ex:
        raise Http404()
    page_settings = {'title': show.seo_title, 'description': show.seo_description}
    context = {'show': show, 'settings': settings, 'page_settings': page_settings}
    return HttpResponse(template.render(context, request))

def page_rewrite(request, page_url):
    try:
        page = Page.objects.get(url=page_url)
    except Exception as ex:
        raise Http404()
    if page.name == 'gifts':
        return gifts(request)
    elif page.name == 'amauters':
        return amauters(request)
    elif page.name == 'birthday':
        return birthday(request)
    elif page.name == 'shedule':
        return shedule(request)
    elif page.name == 'animators':
        return animators(request)
    elif page.name == 'contacts':
        return animators(request)
    elif page.name == 'agreement':	
        return agreement(request)
    elif page.name == 'shares':	
        return shares(request)
    elif page.name == 'guests':	
        return guests(request)
    elif page.name == 'show-programs':
        return show_programs(request)

def show_programs(request):
    settings = Settings.getDict()
    settings['view'] = 'show-programs'
    page = Page.objects.get(name='show-programs')
    shows = Show.objects.order_by('in_construct', 'order')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    page_imgs = {pi['name']: pi['image'] for pi in page.pageimage_set.values()}
    template = loader.get_template('quest/show-programs.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'imgs': page_imgs, 'page_settings': page, 'shows': shows}
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
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'imgs': page_imgs, 'page_settings': page}
    return HttpResponse(template.render(context, request))

def amauters(request):
    settings = Settings.getDict()
    settings['view'] = 'amauters'
    template = loader.get_template('quest/amauters.html')
    page = Page.objects.get(name='amauters')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    page_imgs = {pi['name']: pi['image'] for pi in page.pageimage_set.values()}
    imgs = [{'image': i.image, 'order': i.order, 'title': i.quest.name, 'url': i.quest.getUrl()} for i in
             QuestImage.objects.filter(quest__is_partner=False).filter(type='ama')]
    random.shuffle(imgs)
    imgs2 = list(imgs)
    random.shuffle(imgs2)
    imgs3 = list(imgs)
    random.shuffle(imgs3)

    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'quest_imgs': imgs,
               'page_imgs': page_imgs,
               'quest_imgs2': imgs2,
               'quest_imgs3': imgs3, 'carousel_options': {'certainHeight': False}, 'page_settings': page}
    return HttpResponse(template.render(context, request))

def birthday(request):
    settings = Settings.getDict()
    settings['view'] = 'birthday'
    template = loader.get_template('quest/birthday.html')
    page = Page.objects.get(name='birthday')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = [{'image': i['image'], 'order': i['order'], 'title': i['name']} for i in page.pageimage_set.values('image', 'name', 'order')]
    context = {'settings': settings, 'blocks': page_text_blocks, 'imgs': imgs, 'page_settings': page}
    return HttpResponse(template.render(context, request))

def shedule(request):
    settings = Settings.getDict()
    quests = Quest.objects.order_by('in_construct', 'order')
    discounts = Discount.objects.order_by('order')
    settings['view'] = 'shedule'
    page = Page.objects.get(name='shedule')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = {i['name']: {'image': i['image'], 'order': i['order']} for i in
            page.pageimage_set.values('image', 'name', 'order')}
    template = loader.get_template('quest/shedule.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'quests': quests, 'discounts': discounts,
               'page_settings': page, 'imgs': imgs}
    return HttpResponse(template.render(context, request))

def animators(request):
    settings = Settings.getDict()
    settings['view'] = 'animators'
    page = Page.objects.get(name='animators')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = {i['name']: {'image': i['image'], 'order': i['order']} for i in
            page.pageimage_set.values('image', 'name', 'order')}
    template = loader.get_template('quest/animators.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'page_settings': page, 'imgs': imgs}
    return HttpResponse(template.render(context, request))

def agreement(request):
    settings = Settings.getDict()
    settings['view'] = 'agreement'
    page = Page.objects.get(name='agreement')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = {i['name']: {'image': i['image'], 'order': i['order']} for i in
            page.pageimage_set.values('image', 'name', 'order')}
    template = loader.get_template('quest/agreement.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'page_settings': page, 'imgs': imgs}
    return HttpResponse(template.render(context, request))
	
def guests(request):
	settings = Settings.getDict()
	settings['view'] = 'guests'
	page = Page.objects.get(name='guests')
	page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}	
	imgs = list(page.pageimage_set.order_by('order').values('image', 'name', 'order'))	
	template = loader.get_template('quest/guests.html')
	context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'page_settings': page, 'imgs': imgs, 'imgs_str': json.dumps(imgs)}
	return HttpResponse(template.render(context, request))
	
def shares(request):
    settings = Settings.getDict()
    settings['view'] = 'shares'
    page = Page.objects.get(name='shares')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = {i['name']: {'image': i['image'], 'order': i['order']} for i in
            page.pageimage_set.values('image', 'name', 'order')}
    template = loader.get_template('quest/shares.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'page_settings': page, 'imgs': imgs}
    return HttpResponse(template.render(context, request))
	
def contacts(request):
    settings = Settings.getDict()
    settings['view'] = 'contacts'
    page = Page.objects.get(name='contacts')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    template = loader.get_template('quest/contacts.html')
    context = {'settings': settings, 'page_text_blocks': page_text_blocks, 'page_settings': page}
    return HttpResponse(template.render(context, request))

def ajax_get_visitors(request):
    settings = Settings.getDict()
    return JsonResponse({'visitors': settings.get('visitors_count', None)})

def franchise(request):
    settings = Settings.getDict()
    settings['view'] = 'franchise'
    template = loader.get_template('quest/franchise.html')
    page = Page.objects.get(name='franchise')
    page_text_blocks = {pb['name']: pb['value'] for pb in page.pageblock_set.values()}
    imgs = {i['name']: {'image': i['image'], 'order': i['order']} for i in
            page.pageimage_set.values('image', 'name', 'order')}
    context = {'settings': settings, 'blocks': page_text_blocks, 'imgs': imgs, 'page_settings': page}
    return HttpResponse(template.render(context, request))

def kubik(request):
    settings = Settings.getDict()
    settings['view'] = 'kubik'
    template = loader.get_template('quest/kubik.html')
    context = {'settings': settings}
    return HttpResponse(template.render(context, request))


