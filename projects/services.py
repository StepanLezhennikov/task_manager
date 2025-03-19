from typing import List
from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from tasks.models import Task
from projects.models import Project, ProjectUser
from api.kafka_producer import TOPICS, KafkaProducerService
from projects.serializers import ProjectUserSerializerGet


class ProjectService:
    @staticmethod
    def get_project_users(project_id: int) -> List[ProjectUser]:
        users = ProjectUser.objects.filter(project_id=project_id)
        serializer = ProjectUserSerializerGet(users, many=True)
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
            name = validated_data.get("name")
            description = validated_data.get("description", None)
            logo_url = validated_data.get("logo_url", None)

            project = Project.objects.create(
                name=name, description=description, logo_url=logo_url
            )

            created_tasks_ids = []
            for task_data in validated_data.get("tasks", []):
                created_task = Task.objects.create(project=project, **task_data)

                KafkaProducerService().send_message(
                    {
                        "task_id": created_task.pk,
                        "project_id": project.pk,
                        "status": created_task.status,
                        "created_at": datetime.now().isoformat(),
                    },
                    TOPICS.TASK_CREATED.value,
                )

                created_tasks_ids.append(created_task.pk)

            project_users_ids = []

            created_owner = ProjectUser.objects.create(
                project=project,
                user_id=user_id,
                role=ProjectUser.RoleChoices.OWNER,
            )

            project_users_ids.append(created_owner.pk)

            for project_user_data in validated_data.get("project_users", []):
                created_project_user = ProjectUser.objects.create(
                    project=project, **project_user_data
                )

                KafkaProducerService().send_message(
                    {
                        "user_id": created_project_user.user_id,
                        "project_id": project.pk,
                        "created_at": datetime.now().isoformat(),
                    },
                    TOPICS.USER_ADDED.value,
                )

                project_users_ids.append(created_project_user.pk)

            KafkaProducerService().send_message(
                {
                    "user_id": user_id,
                    "project_id": project.pk,
                    "created_at": datetime.now().isoformat(),
                },
                TOPICS.USER_ADDED.value,
            )

            KafkaProducerService().send_message(
                {
                    "project_id": project.pk,
                    "tasks": created_tasks_ids,
                    "members": project_users_ids,
                    "created_at": datetime.now().isoformat(),
                },
                TOPICS.PROJECT_CREATED.value,
            )

            return project

    @staticmethod
    def get_project_users_by_user_id(user_id: int) -> QuerySet[ProjectUser]:
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        return ProjectUser.objects.filter(project_id__in=project_ids)

    @staticmethod
    def get_users_projects(user_id: int) -> QuerySet[Project]:
        project_ids = list(
            ProjectUser.objects.filter(user_id=user_id).values_list(
                "project_id", flat=True
            )
        )
        return Project.objects.filter(pk__in=project_ids)
