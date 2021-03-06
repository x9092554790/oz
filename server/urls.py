"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
import quest.views
from django.conf.urls.static import static
from django.conf import settings
import views

handler400 = 'server.views.handler400'
handler403 = 'server.views.handler403'
handler404 = 'server.views.handler404'
handler500 = 'server.views.handler500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', quest.views.index, name='index'),
    url(r'^err', views.handler404),
    url(r'^quest/', include('quest.urls')),
    url(r'^show/', include('quest.show_urls')),
    url(r'^', include('quest.urls2')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

