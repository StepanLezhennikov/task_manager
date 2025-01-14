from typing import List

from projects.models import Project, ProjectUser
from projects.serializers import GetProjectUserSerializer


class ProjectService:
    @staticmethod
    def get_project_users(project_id: int) -> List[ProjectUser]:
        users = ProjectUser.objects.filter(project_id=project_id)
        serializer = GetProjectUserSerializer(users, many=True)
        return serializer.data

    @staticmethod
    def get_project_name_by_id(project_id: int) -> str | None:
        try:
            project_name = Project.objects.get(id=project_id).name
        except Project.DoesNotExist:
            return None

        return project_name

    @staticmethod
    def get_project_by_id(project_id: int) -> Project:
        return Project.objects.get(id=project_id)
