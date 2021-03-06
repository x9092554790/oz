from django.contrib import admin
from .models import Quest
from .models import QuestImage
from .models import GoogleDriveDoc
from .models import Settings
from .models import Page
from .models import PageImage
from .models import PageBlock
from .models import Discount
from .models import Video
from django import forms
from .models import Banner
from .models import *


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'type', 'order', 'created')
    fields = ('name', 'type', 'url', 'title', 'content', 'image_tag', 'img', 'video', 'slide_delay', 'order', 'created')
    readonly_fields = ('image_tag', 'image_tag_prev', 'created')

class ShowImageInline(admin.TabularInline):
    model = ShowImage
    fields = ('show', 'name', 'image_tag_prev', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'image_tag_prev', 'created')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    inlines = [ShowImageInline]
    list_display = ('id', 'name', 'desc', 'in_construct', 'order', 'created')
    fields = ('name', 'desc', 'title_desc', 'address', 'phone', 'seo_url', 'seo_title', 'seo_description', 'price_desc', 'players_desc', 'age_desc', 'age_value',
              'players_min', 'players_max', 'players_add', 'duration_min', 'is_new', 'is_with_actor', 'in_construct', 'is_partner', 'is_animator', 'order')
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ShowAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['desc', 'price_desc', 'players_desc', 'age_desc']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

@admin.register(ShowImage)
class ShowImageAdmin(admin.ModelAdmin):
    list_display = ('show', 'name', 'image', 'type', 'order', 'created')
    fields = ('show', 'name', 'image_tag', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'created')


class QuestImageInline(admin.TabularInline):
    model = QuestImage
    fields = ('quest', 'name', 'image_tag_prev', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'image_tag_prev', 'created')

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    inlines = [QuestImageInline]
    list_display = ('id', 'name', 'desc', 'in_construct', 'order', 'created')
    fields = ('name', 'desc', 'title_desc', 'address', 'phone', 'seo_url', 'seo_title', 'seo_description', 'price_desc', 'players_desc', 'age_desc', 'age_value',
              'players_min', 'players_max', 'players_add', 'rating', 'duration_min', 'is_new', 'is_with_actor', 'in_construct', 'is_partner', 'is_animator', 'order')
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(QuestAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['desc', 'price_desc', 'players_desc', 'age_desc']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

@admin.register(QuestImage)
class QuestImageAdmin(admin.ModelAdmin):
    list_display = ('quest', 'name', 'image', 'type', 'order', 'created')
    fields = ('quest', 'name', 'image_tag', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'created')

@admin.register(GoogleDriveDoc)
class GoogleDriveDocAdmin(admin.ModelAdmin):
    pass

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'created')

class PageImageInline(admin.TabularInline):
    model = PageImage
    fields = ('page', 'name', 'image_tag_prev', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'image_tag_prev', 'created')

@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    list_display = ('page', 'name', 'image_tag_prev', 'image', 'type', 'order', 'created')
    fields = ('page', 'name', 'image_tag', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'image_tag_prev', 'created')

class PageBlockInline(admin.TabularInline):
    model = PageBlock
    fields = ('page', 'name', 'value', 'type', 'order', 'created')
    readonly_fields = ('created',)

@admin.register(PageBlock)
class PageBlockAdmin(admin.ModelAdmin):
    list_display = ('page', 'name', 'type', 'order', 'created')
    fields = ('page', 'name', 'value', 'type', 'order', 'created')
    readonly_fields = ('created',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [PageImageInline, PageBlockInline]
    list_display = ('name', 'url', 'created')
    fields = ('name', 'url', 'title', 'description')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'image', 'type', 'order', 'created')
    fields = ('name', 'value', 'desc', 'image_tag', 'image', 'type', 'order', 'created')
    readonly_fields = ('image_tag', 'created')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('quest', 'name', 'type', 'order', 'created')
    fields = ('quest', 'name', 'widget', 'desc', 'type', 'order', 'created')
    readonly_fields = ('created', )

@admin.register(VideoShow)
class VideoShowAdmin(admin.ModelAdmin):
    list_display = ('show', 'name', 'type', 'order', 'created')
    fields = ('show', 'name', 'widget', 'desc', 'type', 'order', 'created')
    readonly_fields = ('created', )