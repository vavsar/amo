from django.urls import path

from .views import get_first_token

urlpatterns = [
    path('get_key/', get_first_token, name='get_first_token')
]
