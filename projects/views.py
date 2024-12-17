from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Project, ProjectUser
from .serializers import ProjectSerializer, ProjectUserSerializer
from .services import ProjectService


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer

    def create_for_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        project = request.data.get('project')
        user_email = "example@gmail.com"  # В будущем интегрировать с микросервисом аутентификации
        role = request.data.get('role')
        if not user_id:
            return Response(
                {"error": "user_id is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_data = {
            "user_id": user_id,
            "user_email": user_email,
            "project": project,
            "role": role
        }

        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user_projects(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = ProjectService.get_user_projects(user_id)
        return Response(data, status=status.HTTP_200_OK)
