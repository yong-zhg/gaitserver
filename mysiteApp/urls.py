# -*- coding: utf-8 -*-

from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
from mysiteApp.views import signup, login, logout, subscribe, info, info_update, password_update

urlpatterns = patterns(
    '',
    url(r'^signup$', signup),
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^subscribe$', subscribe),
    url(r'^info$', info),
    url(r'^info/update$', info_update),
    url(r'^password/update$', password_update),

)

