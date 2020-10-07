"""BootcampCRM URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', include('analytics.urls')),
    path('auth/', include('authentication.urls')),
    path('news/', include('blog.urls')),
    path('', include('courses.urls')),
    path('search/', include('search.urls')),
    path('user/', include('users.urls')),
]
