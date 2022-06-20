from django.urls import path
from project.views import ProjectList, ProjectByID, ContributorList, ContributorDelete

urlpatterns = [
    path('', ProjectList.as_view()),
    path('<int:pk>/', ProjectByID.as_view()),
    path('<int:pk>/users/', ContributorList.as_view()),
    path('<int:pk>/users/<int:pk_user>', ContributorDelete.as_view()),
]
