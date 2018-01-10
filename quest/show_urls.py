from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<show_name>[a-zA-Z0-9-]+)/$', views.show_rewrite, name='show-rewrite'),
]