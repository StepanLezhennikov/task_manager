from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, ProjectUser
from .serializers import ProjectSerializer, ProjectUserSerializer
from .services import ProjectService
from .permissions import IsProjectOwnerOrReadOnly, IsProjectUserOwnerOrReader
from .tasks import send_email_invite


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает только проекты, к которым пользователь имеет доступ.
        """
        user_id = self.request.user_id
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list('project_id', flat=True)
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
            role="owner"
        )


class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [IsProjectUserOwnerOrReader]

    def get_queryset(self):
        """
        Возвращает список участников проекта, доступных текущему пользователю.
        """
        user_id = self.request.user_id
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list('project_id', flat=True)
        return ProjectUser.objects.filter(project_id__in=project_ids)

    @action(detail=True, methods=['POST'], name='add-user-to-project')
    def add_user_to_project(self, request, *args, **kwargs):
        """Добавление пользователя в проект"""

        added_user_id = kwargs.get('user_id')
        project_id = request.data.get('project')
        user_email = "example@gmail.com"  # В будущем интегрировать с микросервисом аутентификации
        role = request.data.get('role')

        if not added_user_id:
            return Response(
                {"error": "added_user_id is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            owner_id = ProjectUser.objects.get(project=project_id, role="owner").user_id
        except :
            return Response(
                {"error": "Project does not exist or you have no access to this project."},
                status=status.HTTP_404_NOT_FOUND
            )
        print("owner_id", owner_id)
        print("request.user_id", request.user_id)
        if owner_id != request.user_id:
            print('ping')
            return Response(
                {"error": "Only the project owner can add users."},
                status=status.HTTP_403_FORBIDDEN
            )


        user_data = {
            "user_id": added_user_id,
            "user_email": user_email,
            "project": project_id,
            "role": role
        }


        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            serializer.save(user_id=added_user_id)
            subject = f"You have been added to a project"
            message = f"You have been added to a project {serializer.data['project']}"
            from_email = 'stepanlezennikov@gmail.com'
            recipient_list = ['stepanlezennikov@gmail.com']
            # print(subject, message, from_email, recipient_list)
            send_email_invite.delay(subject, message, from_email, recipient_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['GET'])
    def get_project_users(self, request, *args, **kwargs):
        """Просмотр пользователей на проекте"""
        user_id = request.user_id
        project_id = kwargs.get('project_id')

        if not Project.objects.filter(id=project_id).exists():
            return Response(
                {"error": "Project does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user_id:
            return Response(
                {"error": "user_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_id not in ProjectUser.objects.filter(project_id=project_id).values_list('user_id', flat=True):
            return Response(
                {"error": "You do not have access to this project."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = ProjectService.get_project_users(user_id)
        return Response(data, status=status.HTTP_200_OK)
