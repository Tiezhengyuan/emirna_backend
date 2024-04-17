from time import sleep
import subprocess
from django.conf import settings
from celery import shared_task, current_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from .schedule_tasks import ScheduleTasks

'''
scheduled tasks defined in settings
they are automatically launched with django
'''
@shared_task
def schedule_task():
  res = ScheduleTasks().run_task()
  return res

'''
celery tasks
'''
@shared_task
def execute_tasks(project_id):
  print('########', project_id)
  from pipelines import ExecuteTasks
  # pass celery task id to django
  celery_task_id = current_task.request.get('id')
  res = ExecuteTasks(project_id, celery_task_id, None, True)()
  logger.info(f"Try to launch execute_task. project={project_id}")
  return res 

@shared_task
def download_genome(data_source, specie_name, version):
  from pipelines import ProcessGenome
  p = ProcessGenome(data_source, specie_name, version)
  return p.download_genome()


@shared_task
def scan_raw_data():
  from pipelines import ProcessRawData
  return ProcessRawData().scan_raw_data()

@shared_task
def refresh_raw_data():
  from pipelines import ProcessRawData
  return ProcessRawData().refresh_raw_data()

@shared_task
def parse_sample_data(study_name, prefix=None, postfix=None):
  from pipelines import ProcessRawData
  c = ProcessRawData()
  return c.parse_sample_data(study_name, prefix, postfix)

@shared_task
def reset_sample():
  from pipelines import ProcessRawData
  return ProcessRawData().reset_sample()

@shared_task
def trim_adapter(params):
  from pipelines import TrimAdapter
  return TrimAdapter(params)()

@shared_task
def build_index(data_source, specie, version, aligner):
  from pipelines import Align
  c = Align(aligner)
  return c.build_index(data_source, specie, version)



# for debugging
@shared_task
def minus(x,y):
  print(x,y)
  return x*y
