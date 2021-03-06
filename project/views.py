from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.models import Project, Contributor
from project.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from core.models import User
from .permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions
from .models import Issue, Comment


class ProjectList(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def list(self, request, *args, **kwargs):
        contributors = [i.project_id for i in Contributor.objects.filter(user_id=self.request.user)]
        serializer = ProjectSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['author_user_id'] = request.user.id
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(user_id=request.user, project_id=project, role='AUTHOR')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectByID(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]
    lookup_field = 'pk'

    def list(self, pk):
        queryset = self.get_queryset().filter(id=pk)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs["pk"])
        data = request.data.copy()
        data['author_user_id'] = project.author_user_id.id
        serializer = self.get_serializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        project.delete()
        return Response("Project has been deleted.", status=status.HTTP_204_NO_CONTENT)


class ContributorList(ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermissions]
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs["pk"])
        data = request.data.copy()
        data['project_id'] = project.id
        print(data)
        try:
            Contributor.objects.get(user_id=data['user_id'], project_id=project.id)
            return Response("User has already been added", status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data['user_id'])
                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response("This User does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs["pk"])
        contributor = Contributor.objects.filter(project_id=project.id)
        serializer = self.get_serializer(contributor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContributorDelete(DestroyAPIView):
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def delete(self, request, *args, **kwargs):
        contributor = get_object_or_404(Contributor, user_id=self.kwargs['pk_user'], project_id=self.kwargs['pk'])
        if contributor.role == "AUTHOR":
            return Response("Author cannot be deleted.", status=status.HTTP_400_BAD_REQUEST)
        contributor.delete()
        return Response("Contributor has been deleted.", status=status.HTTP_204_NO_CONTENT)


class IssueList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IssuePermissions]

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        queryset = Issue.objects.filter(project_id=project.id)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        data = request.data.copy()
        data['project_id'] = project.id
        data['author_user_id'] = request.user.id
        try:
            Contributor.objects.get(user_id=data["assignee_user_id"], project_id=project.id)
            serializer = IssueSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response("This user has not permissions or does not exist", status=status.HTTP_400_BAD_REQUEST)


class IssueUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IssuePermissions]

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        issue = get_object_or_404(Issue, id=kwargs['pk_issue'])
        data = request.data.copy()
        data['project_id'] = project.id
        data['author_user_id'] = request.user.id
        try:
            Contributor.objects.get(user_id=data["assignee_user_id"], project_id=project.id)
            serializer = IssueSerializer(issue, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response("This user has not permissions or does not exist", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs['pk_issue'])
        issue.delete()
        return Response("Issue successfully deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, CommentPermissions])
def comment_list(request, pk, pk_issue):
    get_object_or_404(Project, id=pk)
    issue = get_object_or_404(Issue, id=pk_issue)

    if request.method == 'GET':
        comments = Comment.objects.filter(issue_id=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        data['issue_id'] = issue.id
        data['author_user_id'] = request.user.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, CommentPermissions])
def comment_detail(request, pk, pk_issue, pk_comment):
    get_object_or_404(Project, id=pk)
    issue = get_object_or_404(Issue, id=pk_issue)
    comment = get_object_or_404(Comment, id=pk_comment)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['issue_id'] = issue.id
        data['author_user_id'] = comment.author_user_id.id

        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response('Comment successfully deleted.', status=status.HTTP_204_NO_CONTENT)
