from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from projects.models import Project, ProjectUser
from projects.services import ProjectService
from projects.permissions import (
    HasAccessToProject,
    IsProjectUserOwner,
    IsProjectUserReader,
)
from projects.serializers import ProjectSerializer, ProjectUserSerializer
from notifications.services import NotificationService


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectUserOwner | IsProjectUserReader]

    def get_queryset(self):
        """
        Возвращает только проекты, к которым пользователь имеет доступ.
        """
        user_id = self.request.user_id
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        return Project.objects.filter(id__in=project_ids)

    def perform_create(self, serializer):
        """
        Создает проект и автоматически назначает пользователя владельцем.
        """
        project = serializer.save()
        ProjectUser.objects.create(
            project=project,
            user_id=self.request.user_id,
            user_email=self.request.user_email,
            role="owner",
        )


class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [IsProjectUserOwner | IsProjectUserReader]

    def get_queryset(self):
        """
        Возвращает список участников проекта, доступных текущему пользователю.
        """
        user_id = self.request.user_id
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        return ProjectUser.objects.filter(project_id__in=project_ids)

    @action(
        detail=True,
        methods=["POST"],
        name="add-user-to-project",
        permission_classes=[HasAccessToProject],
    )
    def add_user_to_project(self, request, *args, **kwargs) -> Response:
        """Добавление пользователя в проект"""

        added_user_id = kwargs.get("user_id")
        project_id = request.data.get("project")

        project = ProjectService.get_project_by_id(project_id)
        if not project.name:
            return Response(
                {
                    "error": "Project does not exist or you have no access to this project."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user_email = "example@gmail.com"  # В будущем интегрировать с микросервисом аутентификации
        role = request.data.get("role")

        user_data = {
            "user_id": added_user_id,
            "user_email": user_email,
            "project": project_id,
            "role": role,
        }

        self.check_object_permissions(request, project)

        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            serializer.save(user_id=added_user_id)
            NotificationService.send_invite_email(
                from_user_email=request.user_email,
                project_name=project.name,
                recipient_list=["stepanlezennikov@gmail.com"],
            )  # Change email later
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def get_project_users(self, request, *args, **kwargs) -> Response:
        """Просмотр пользователей на проекте"""
        user_id = request.user_id
        project_id = kwargs.get("project_id")

        project = get_object_or_404(Project, id=project_id)

        if not user_id:
            return Response(
                {"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user_id not in project.project_users.all().values_list("user_id", flat=True):
            return Response(
                {"error": "You do not have access to this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = ProjectService.get_project_users(project_id)
        return Response(data, status=status.HTTP_200_OK)
