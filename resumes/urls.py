from django.urls import path
from .views import ResumeApiView, ResumeDetailApiView

urlpatterns = [
    path('api/', ResumeApiView.as_view(), name='resume_api'),
    path('api/<uuid:uid>/', ResumeDetailApiView.as_view(), name='resume_detail_api'),
]
