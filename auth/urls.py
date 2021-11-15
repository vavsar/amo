from django.urls import path

from .views import get_token


path('get_key/', get_token, name='get_key')