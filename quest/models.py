from __future__ import unicode_literals
from django.db import models
import django.utils.html
import datetime
from django.conf import settings as app_settings

class Quest(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=4096)
    price_desc = models.CharField(max_length=4096, default="")
    players_desc = models.CharField(max_length=4096, default="")
    age_desc = models.CharField(max_length=4096, default="")
    age_value = models.IntegerField(default=0)
    players_min = models.IntegerField(default=2)
    players_max = models.IntegerField(default=4)
    rating = models.DecimalField(default=100.0, decimal_places=2, max_digits=5)
    duration_min = models.IntegerField(default=60)
    in_construct = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created = models.DateTimeField('date created', auto_now_add=True)

    def getLogo(self):
        logo = self.questimage_set.get(type="logo")
        return logo.image if logo else None

    def getImgs(self):
        imgs = self.questimage_set.filter(type='ama').order_by('order')
        if not len(imgs):
            imgs = self.questimage_set.filter(type="logo")
        return imgs

    def getQuestVid(self):
        vid = list(self.video_set.filter(type='quest_video')[:1])
        if vid:
            return vid[0]
        return None

    def getFirstImg(self):
        imgs = self.questimage_set.get(type='img', order='1')
        return imgs

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

def quest_image_directory_path(instance, filename):
    return 'quest_{0}/{1}'.format(instance.quest.id, instance.name)

class QuestImage(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=quest_image_directory_path)
    type = models.CharField(max_length=100, null=True)
    order = models.IntegerField(default=1)
    created = models.DateTimeField('date created', auto_now_add=True)

    def image_tag(self):
        return django.utils.html.format_html(u'<img src="/media/{}" />', self.image)
    image_tag.short_description = "Preview"

    def image_tag_prev(self):
        return django.utils.html.format_html(u'<img style="height: 50px; object-fit: cover;" src="/media/{}" />',
                                             self.image)
    image_tag_prev.short_description = "Small Preview"

    def __str__(self):
        return "%s-%s" % (self.quest.name, self.name)

    def __unicode__(self):
        return u"%s-%s" % (self.quest.name, self.name)

class Page(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created = models.DateTimeField('date created', auto_now_add=True)
    def __str__(self):
        return self.name

def page_image_directory_path(instance, filename):
    return 'page_{0}/{1}'.format(instance.page.name, instance.name)

class PageImage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=page_image_directory_path)
    type = models.CharField(max_length=100, null=True)
    order = models.IntegerField(default=1)
    created = models.DateTimeField('date created', auto_now_add=True)

    def image_tag(self):
        return django.utils.html.format_html(u'<img src="/media/{}" />', self.image)
    image_tag.short_description = "Preview"

    def image_tag_prev(self):
        return django.utils.html.format_html(u'<img style="height: 50px; object-fit: cover;" src="/media/{}" />', self.image)
    image_tag_prev.short_description = "Small Preview"

    def __str__(self):
        return "%s-%s" % (self.page.name, self.name)

    def __unicode__(self):
        return u"%s-%s" % (self.page.name, self.name)


class PageBlock(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.TextField(max_length=4096)
    type = models.CharField(max_length=100, null=True)
    order = models.IntegerField(default=1)
    created = models.DateTimeField('date created', auto_now_add=True)

class GoogleDriveDoc(models.Model):
    TYPES = (
        ('img-p', 'Image of Players'),
        ('img-o', 'Image of Other'),
    )
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPES)
    created = models.DateTimeField('date created', auto_now_add=True)

class Settings(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created = models.DateTimeField('date created', auto_now_add=True)

    @staticmethod
    def getDict():
        return {v['name']: v['value'] for v in Settings.objects.values()}


def discount_image_directory_path(instance, filename):
    return 'discount_{0}'.format(instance.id)

class Discount(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    def getPerUrl(self):
        return "quest/imgs/per-%s.png" % (self.value,)
    desc = models.TextField(max_length=4096, default='')
    image = models.ImageField(upload_to=discount_image_directory_path)
    def image_tag(self):
        return django.utils.html.format_html(u'<img src="/media/{}" />', self.image)
    image_tag.short_description = "Preview"
    type = models.CharField(max_length=100, null=True)
    order = models.IntegerField(default=1)
    created = models.DateTimeField('date created', auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Video(models.Model):
    name = models.CharField(max_length=100)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    widget = models.TextField(max_length=4096)
    desc = models.TextField(max_length=4096, default='')
    type = models.CharField(max_length=100, null=True)
    order = models.IntegerField(default=1)
    created = models.DateTimeField('date created', auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
