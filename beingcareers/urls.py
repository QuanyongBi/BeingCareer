
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    path('users/', include('users.urls')),
    path('resumes/', include('resumes.urls')),
    path('jobs/', include('jobs.urls')),
]
