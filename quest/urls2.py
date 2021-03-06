from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gifts', views.gifts, name='gifts'),
    url(r'^amauters', views.amauters, name='amauters'),
    url(r'^birthday', views.birthday, name='birthday'),
    url(r'^shedule', views.shedule, name='shedule'),
    url(r'^animators', views.animators, name='animators'),
    url(r'^contacts', views.contacts, name='contacts'),
    url(r'^franchise', views.franchise, name='franchise'),

    url(r'^ajax_get_visitors', views.ajax_get_visitors, name='ajax_get_visitors'),

    url(r'^(?P<page_url>[A-Za-z0-9-]+)$', views.page_rewrite, name='page_rewrite'),

    url(r'^kubik', views.kubik, name='kubik'),
]