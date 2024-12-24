from projects.models import ProjectUser, Project
from projects.serializers import ProjectSerializer, GetProjectUserSerializer


class ProjectService:
    @staticmethod
    def get_project_users(project_id):
        users = ProjectUser.objects.filter(project_id=project_id)
        serializer = GetProjectUserSerializer(users, many=True)
        return serializer.data
