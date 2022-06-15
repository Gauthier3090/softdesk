from django.urls import path
from project.views import ProjectList

urlpatterns = [
    path('', ProjectList.as_view(), name='projects'),
]
