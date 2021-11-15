from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('app/', include('auth.urls')),
    path('auth/', include('django.contrib.auth.urls'))
]