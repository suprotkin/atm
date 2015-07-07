__author__ = 'roman'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'error/$', views.ErrorPage.as_view(), name='error'),
]
