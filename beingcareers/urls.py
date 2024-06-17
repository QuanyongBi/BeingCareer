
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('resumes/', include('resumes.urls')),
    path('jobs/', include('jobs.urls')),
]
