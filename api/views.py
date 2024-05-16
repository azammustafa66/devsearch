from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid

from .serializers import *
from projects.models import Project


@api_view(["GET"])
def get_routes(request: HttpRequest):
    routes = [
        {"GET": "/api/v1/projects/"},
        {"GET": "/api/v1/projects/1"},
        {"POST": "/api/v1/projects/vote"},
        {"POST": "/api/v1/users/token"},
        {"DELETE": "/api/v1/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_projects(request: HttpRequest):
    projects = Project.objects.all()
    project_serializer = ProjectSerializer(projects, many=True)
    return Response(project_serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_project(request: HttpRequest, pk: uuid.UUID):
    project = Project.objects.get(id=pk)
    project_serializer = ProjectSerializer(project, many=False)
    return Response(project_serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vote_project(request: HttpRequest, pk: uuid.UUID):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    serializer = ProjectSerializer(project, many=False)

    review, created = Review.objects.get_or_create(owner=user, project=project)
    review.value = data["value"]
    review.save()
    project.get_vote_count

    return Response(serializer.data)
