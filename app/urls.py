from django.urls import path

from .views import get_contact


urlpatterns = [
    path('get_contact/', get_contact, name='get_contact'),
]
