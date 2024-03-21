'''
executions by project triggered by erna-app.py or frontend
'''
import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from .project import Project


class ProjectExecutionManager(models.Manager):
    def start(self, project_id:str, celery_task_id:str=None):
        '''
        run/execute a project
        '''
        project = Project.objects.get(project_id=project_id)
        obj = self.model.objects.create(
            project=project,
            start_time=timezone.now(),
            celery_task_id=celery_task_id,
        )
        # update Project status
        project.update_status('locked')
        return obj

    def project_executions(self, project_id:str):
        project = Project.objects.get(project_id=project_id)
        executions = self.filter(project=project)
        res = [{'value': obj.start_time, 'text': obj.to_dict()} \
            for obj in executions]
        return res

class ProjectExecution(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()
    # celery task is triggered by front-end
    celery_task_id = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    # should be updated once execution is done
    end_time = models.DateTimeField(blank=True, null=True)

    objects = ProjectExecutionManager()

    class Meta:
        app_label = 'rna_seq'
        ordering = ['project',]

    @property
    def log_path(self):
        '''
        one project execution, one log file
        '''
        file_name = f"{self.celery_task_id}.log"
        return os.path.join(settings.LOGS_DIR, file_name)

    def to_dict(self):
        return {
            'project_id': self.project.project_id,
            'log_path': self.log_path,
            'celery_task_id': self.celery_task_id,
        }
    
    def finish(self):
        self.end_time = timezone.now()
        self.save()
        # update Project status
        self.project.update_status('ready')
        return self.end_time - self.start_time

