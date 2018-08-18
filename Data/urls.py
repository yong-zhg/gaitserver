__author__ = 'Jianming'

# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
from Data.views import *

urlpatterns = patterns(
    '',
    url(r'^upload$', data_upload),
    url(r'^daily/upload$', daily_data_upload),
    url(r'^query$', data_query),
    url(r'^pressure/query$', data_pressures_query),
    url(r'^acceleration/query$', data_acceleration_query),
    url(r'^angleacceleration/query$', data_angleAcceleration_query),
    url(r'^step/query$', data_steps_query),
    url(r'^signal/query$', data_signal_query),

    url(r'^pressure/query/pages$', data_pressures_query_pages),
    url(r'^acceleration/query/pages$', data_acceleration_query_pages),
    url(r'^angleacceleration/query/pages$', data_angleAcceleration_query_pages),
    url(r'^step/query/pages$', data_steps_query_pages),
    url(r'^signal/query/pages$', data_signal_query_pages),

    url(r'^pressure/pages/count$', data_pressures_count),
    url(r'^acceleration/pages/count$', data_acceleration_count),
    url(r'^angleacceleration/pages/count$', data_angleAcceleration_count),
    url(r'^step/pages/count$', data_steps_count),
    url(r'^signal/pages/count$', data_signal_count),
)

