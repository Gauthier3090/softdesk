from django.urls import path
from project.views import ProjectList, ProjectByID, ContributorList, ContributorDelete, IssueList, IssueUpdateDestroy

urlpatterns = [
    path('', ProjectList.as_view()),
    path('<int:pk>/', ProjectByID.as_view()),
    path('<int:pk>/users/', ContributorList.as_view()),
    path('<int:pk>/users/<int:pk_user>', ContributorDelete.as_view()),
    path('<int:pk>/issues/', IssueList.as_view()),
    path('<int:pk>/issues/<int:pk_issue>', IssueUpdateDestroy.as_view())
]
