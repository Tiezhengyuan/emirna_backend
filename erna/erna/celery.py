import os
import sys
from celery import Celery
from celery.signals import setup_logging, after_setup_task_logger, task_prerun, task_postrun
from celery.app.log import TaskFormatter
import logging

ernav2_dir = os.path.dirname(
  os.path.dirname(os.path.dirname(__file__))
)
sys.path.append(ernav2_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erna.settings')

app = Celery('erna');
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
  print(f'Reqyest: {self.request}')

# override the logging with own
# @setup_logging.connect
# def config_loggers(*args, **kwargs):
#     from logging.config import dictConfig
#     from django.conf import settings

#     dictConfig(settings.LOGGING)

# @after_setup_task_logger.connect
# def setup_task_logger(logger, *args, **kwargs):
#   fh = logging.FileHandler(f'/home/yuan/bio/emirna_backend/logs/default.log')
#   fh.setLevel(logging.DEBUG)
#   fr = TaskFormatter('%(asctime)s | %(task_id)s | %(levelname)s | %(message)s')
#   fh.setFormatter(fr)
#   logger.addHandler(fh)

@task_prerun.connect
def overload_task_logger(task_id, task, args, **kwargs):
  logger = logging.getLogger("celery.task")
  file_handler = logging.FileHandler(f'/home/yuan/bio/emirna_backend/logs/{task_id}.log')
  file_handler.setLevel(logging.INFO)
  tf = TaskFormatter("%(asctime)s | %(levelname)s | %(processName)s | %(task_name)s | %(task_id)s | %(message)s")
  file_handler.setFormatter(tf)
  logger.addHandler(file_handler)

@task_postrun.connect
def cleanup_logger(task_id, task, args, **kwargs):
  logger = logging.getLogger("celery.task")
  log_path = f'/home/yuan/bio/emirna_backend/logs/{task_id}.log'
  for handler in logger.handlers:
    if isinstance(handler, logging.FileHandler) and handler.baseFilename == log_path:
      logger.removeHandler(handler)