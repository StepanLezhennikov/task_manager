from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from notifications.services import NotificationService

from .models import Project, ProjectUser
from .services import ProjectService
from .permissions import IsProjectOwnerOrReadOnly, IsProjectUserOwnerOrReader
from .serializers import ProjectSerializer, ProjectUserSerializer


class BaseProjectViewSet(viewsets.ModelViewSet):
    def has_access_to_project(self, user_id, project_id):
        return ProjectUser.objects.filter(
            user_id=user_id, project_id=project_id
        ).exists()


class ProjectViewSet(BaseProjectViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwnerOrReadOnly]

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


class ProjectUserViewSet(BaseProjectViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [IsProjectUserOwnerOrReader]

    def get_queryset(self):
        """
        Возвращает список участников проекта, доступных текущему пользователю.
        """
        user_id = self.request.user_id
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        return ProjectUser.objects.filter(project_id__in=project_ids)

    @action(detail=True, methods=["POST"], name="add-user-to-project")
    def add_user_to_project(self, request, *args, **kwargs):
        """Добавление пользователя в проект"""

        added_user_id = kwargs.get("user_id")
        project_id = request.data.get("project")

        project_name = ProjectService.get_project_name_by_id(project_id)
        if not project_name:
            return Response(
                {
                    "error": "Project does not exist or you have no access to this project."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user_email = "example@gmail.com"  # В будущем интегрировать с микросервисом аутентификации
        role = request.data.get("role")

        if not self.has_access_to_project(request.user_id, project_id):
            return Response(
                {"error": "You do not have access to this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user_data = {
            "user_id": added_user_id,
            "user_email": user_email,
            "project": project_id,
            "role": role,
        }

        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            serializer.save(user_id=added_user_id)
            NotificationService.send_invite_email(
                from_user_email=request.user_email,
                project_name=project_name,
                recipient_list=["stepanlezennikov@gmail.com"],
            )  # Change email later
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def get_project_users(self, request, *args, **kwargs):
        """Просмотр пользователей на проекте"""
        user_id = request.user_id
        project_id = kwargs.get("project_id")

        if not Project.objects.filter(id=project_id).exists():
            return Response(
                {"error": "Project does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        if not user_id:
            return Response(
                {"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user_id not in ProjectUser.objects.filter(project_id=project_id).values_list(
            "user_id", flat=True
        ):
            return Response(
                {"error": "You do not have access to this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = ProjectService.get_project_users(user_id)
        return Response(data, status=status.HTTP_200_OK)
