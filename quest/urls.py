from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<quest_id>[0-9]+)/$', views.quest, name='quest'),


    url(r'^get_remain_imgs', views.quest_get_remain_imgs, name='quest_get_remain_imgs'),
    url(r'^google_doc_get_random_player_images', views.google_doc_get_random_player_images, name='google_doc_get_random_player_images'),
    url(r'^gifts', views.gifts, name='gifts'),
    url(r'^amauters', views.amauters, name='amauters'),
    url(r'^birthday', views.birthday, name='birthday'),
    url(r'^shedule', views.shedule, name='shedule'),
    url(r'^animators', views.animators, name='animators'),
    url(r'^contacts', views.contacts, name='contacts'),
    url(r'^frinchise', views.franchise, name='franchise'),


    url(r'^(?P<quest_name>[a-zA-Z0-9-]+)/$', views.quest_rewrite, name='quest-rewrite'),
]