# -*- coding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import *
from Data.urls import *
from mysiteApp.velocity import velocity
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/static/index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('mysiteApp.urls')),
    url(r'^data/', include('Data.urls')),
    url(r'^velocity', velocity),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += patterns(
#     'mysiteApp.views',
#     url(r'^test_json/$', 'test_json'),
#     """
#     (r'^signup/$', 'signup'),
#     (r'^login/$', 'login'),
#     (r'^logout/$', 'logout'),
#     (r'^index/$', 'index')
#     """
# )
