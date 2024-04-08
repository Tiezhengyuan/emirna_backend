'''
sequence alignment
'''
import os
from django.conf import settings
from rnaseqdata import dump_seqdata

import rna_seq.models
from rna_seq.models import Genome, AlignerIndex, Tool
from .process import Process
from .process_cmd import ProcessCMD

EXTERNALS_DIR = getattr(settings, 'EXTERNALS_DIR')
REFERENCES_DIR = getattr(settings, 'REFERENCES_DIR')

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


class Align:
  def __init__(self, params:dict=None):
    self.params = params if params else {}

  # used by erna_app.py
  def index_builder(self, specie:str, genome_version:str, \
      aligner:str, aligner_version:str) -> None:
    '''
    update self.params for building index
    if none is passed to self.params
    '''
    #get Genome
    genome = Genome.objects.get_genome(specie, genome_version)
    self.params['genome'] = genome

    # get Tool
    aligner_map = {
      'bowtie': 'bowtie2-build',
      'hisat2': 'hisat2-build',
      'STAR': 'STAR',
    }
    if aligner_map.get(aligner):
      self.params['tool'] = Tool.objects.get(
        tool_name=aligner,
        version=aligner_version,
        exe_name=aligner_map[aligner]
      )
    return None
  
  '''
  build index
  '''
  def build_index(self):
    '''
    method: build_index
    '''
    tool = self.params.get('tool')
    if tool is None:
      return None

    # get annotations from RNA or other models
    task_params = self.params['task'].get_params()
    this_model = getattr(rna_seq.models, task_params['model'])
    obj = this_model.objects.get(pk=task_params['id']) if 'id' in task_params \
      else this_model.objects.get(**task_params['query'])
    
    # update seqdata
    if hasattr(obj, 'annot_json') and obj.annot_json:
      self.params['seqdata'].put_variables(obj.annot_json)
      dump_seqdata(self.params['seqdata'], self.params['seqdata_path'])

    # build index
    index_path = obj.get_index_path(tool)
    meta_data = {
      'fa_path': obj.file_path,
      'index_path': index_path,
      'model_name': task_params['model'],
      'model_id': task_params.get('id'),
      'model_query': task_params.get('query'),
      'tool_query': {
        'exe_name': tool.exe_name,
        'version': tool.version,
      },
    }
    if not index_path:
      new_index = AlignerIndex.objects.new_index(tool, obj, meta_data)
      self.params['cmd'] = ProcessCMD.aligner_build_index(tool, meta_data)
      Process.run_subprocess(self.params)
      new_index.update_index(meta_data)
    self.params['output'].append(meta_data)
    return None



  def get_index_path(self):
    '''
    get index for aligner
    '''
    # Firstly check Task.params
    if self.params.get('task') and self.params['task'].get_params():
      index_path = self.params['task'].get_params().get('index_path')
      if index_path:
        logger.info(f"Get index path from task.params.")
        return index_path
    
    # secondly check its parent TaskExecution
    if self.params.get('parent_params'):
      logger.info(f"Get index path form parent_params={self.params['parent_params']}.")
      parent_output = self.params['parent_params']['output']
      for item in parent_output:
        if 'index_path' in item:
          return item['index_path']

    # Finally check its execution of parent Task
    for parent_output in self.params['parent_outputs']:
      if 'index_path' in parent_output:
        logger.info(f"Get index path from parent_outputs={parent_output}")
        return parent_output['index_path']
    return None


  '''
  sequence alignment
  '''
  def align(self):
    '''
    '''
    tool = self.params.get('tool')
    if tool is None:
      return None
    
    sample_files = self.params['parent_outputs']
    for meta_data in sample_files:
      sample_name = meta_data['sample_name']
      output_prefix = os.path.join(self.params['output_dir'], sample_name)
      meta_data['index_path'] = self.get_index_path()
      meta_data['output_prefix'] = output_prefix

      # build CMD
      exe_name = self.params['tool'].exe_name
      if exe_name == 'bowtie2':
        self.params['cmd'] = ProcessCMD.bowtie2_align(tool, meta_data)

      # run process
      Process.run_subprocess(self.params)

      # update params['output']
      self.params['output_prefix'] = output_prefix
      self.params['output'].append(meta_data)
    return None


