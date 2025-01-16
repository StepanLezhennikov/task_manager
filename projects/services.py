from typing import List

from django.db import transaction

from tasks.models import Task
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

    @staticmethod
    def create_project_with_users_and_tasks(
        validated_data: dict, user_id: int
    ) -> Project:
        """
        Creates a new project, assigns the current user as the owner,
        and creates associated tasks and project users.
        """
        with transaction.atomic():
            name = validated_data.pop("name")
            description = validated_data.pop("description", None)
            logo_url = validated_data.pop("logo_url", None)

            project = Project.objects.create(
                name=name, description=description, logo_url=logo_url
            )

            for task_data in validated_data.pop("tasks", []):
                Task.objects.create(project=project, **task_data)

            for project_user_data in validated_data.pop("project_users", []):
                ProjectUser.objects.create(project=project, **project_user_data)

            ProjectUser.objects.create(
                project=project,
                user_id=user_id,
                role=ProjectUser.RoleChoices.OWNER,
            )

            return project

    @staticmethod
    def get_project_users_by_user_id(user_id: int) -> List[ProjectUser]:
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        return list(ProjectUser.objects.filter(project_id__in=project_ids))

    @staticmethod
    def get_users_projects(user_id: int) -> List[Project]:
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        return list(Project.objects.filter(id__in=project_ids))
