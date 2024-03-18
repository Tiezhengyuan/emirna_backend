'''
retrieve data for further analysis
'''
from rna_seq.models import SampleProject


class Collect:
  def __init__(self, params:dict):
    self.params = params

  def import_data(self):
    '''
    launched by task T00
    '''
    # get same ~ raw data
    self.import_sample_data()

  def import_sample_data(self):
    self.params['sample_files'] = SampleProject.objects.sample_files(self.params['project'])
    paths = SampleProject.objects.sample_files_path(self.params['project'])
    self.params['output'] += paths


      
