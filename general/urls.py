"""BootcampCRM URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', include('apps.analytics.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('news/', include('apps.blog.urls')),
    path('', include('apps.courses.urls')),
    path('search/', include('apps.search.urls')),
    path('user/', include('apps.users.urls')),
]
