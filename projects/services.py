from projects.models import ProjectUser, Project
from projects.serializers import ProjectSerializer


class ProjectService:
    @staticmethod
    def get_user_projects(user_id):
        project_ids = ProjectUser.objects.filter(user_id=user_id).values_list('project_id', flat=True)
        projects = Project.objects.filter(id__in=project_ids).prefetch_related('tasks', 'project_users')
        serializer = ProjectSerializer(projects, many=True)
        return serializer.data
