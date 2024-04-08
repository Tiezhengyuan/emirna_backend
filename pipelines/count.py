'''
retrieve data for further analysis
'''
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from biofile import GFF
import os
import pandas as pd
import pysam
from rnaseqdata import NodeData, dump_seqdata
from typing import Iterable

class Count:
    def __init__(self, params:dict):
        self.params = params

    def merge_read_counts(self):
        '''
        method: merge_read_counts
        '''
        rc_files = self.scan_rc_files()
        # merge RC.txt if they exist
        if rc_files:
            self.merge_rc_files(rc_files)
        # update seqdata.obj
        dump_seqdata(self.params['seqdata'], self.params['seqdata_path'])
        return None

    def scan_rc_files(self) -> Iterable:
        rc_files = []
        for parent in self.params['parents']:
            outputs = parent.task_execution.get_output()
            for output in outputs:
                if 'RC' in output:
                    path = (output['sample_name'], output['RC'])
                    rc_files.append(path)
        return rc_files
                    
   
    def merge_rc_files(self, rc_files:list):
        '''
        merge multiple RC files into RC.txt
        '''
        # update SeqData
        rc_node = NodeData(self.params['seqdata'].root, 'RC')
        for sample_name, rc_file in rc_files:
            rc = pd.read_csv(rc_file, sep='\t', index_col=0, header=0)
            rc.name = sample_name
            rc_node.put_data(rc.iloc[:,0])
        self.params['seqdata'].nodes['RC'] = rc_node

        # export
        df = self.params['seqdata'].to_df('RC', 1)
        outfile = os.path.join(self.params['output_dir'], 'RC.txt')
        df.to_csv(outfile, sep='\t', index=True, header=True)
        meta = {
            'count': 'RC',
            'RC': outfile,
            'shape': df.shape,
        }
        df = df.T
        self.params['output'].append(meta)
        outfile = os.path.join(self.params['output_dir'], 'RC_T.txt')
        df.to_csv(outfile, sep='\t', index=False, header=True)
        meta = {
            'count': 'RC',
            'RC': outfile,
            'shape': df.shape,
        }
        self.params['output'].append(meta)
        return rc_node


    def count_reads(self):
        '''
        reads counting from *.sam
        '''
        # filter read counts. at least 2
        min_counts = self.params.get('min_counts')
        if min_counts is None or min_counts < 2:
            min_counts = 2
        
        for parent in self.params['parents']:
            output = parent.task_execution.get_output()
            for item in [i for i in output if 'sam_file' in i]:
                sample_name = item['sample_name']
                output_prefix = os.path.join(self.params['output_dir'], sample_name)
                unaligned_file = output_prefix + ".unaligned.fa"
                rc = self.analyze_samfile(item['sam_file'], unaligned_file)
                # to txt
                df = pd.DataFrame.from_dict(rc, orient='index', columns=[sample_name,])
                df = df[df[sample_name]>=min_counts]
                outfile = output_prefix + ".RC.txt"
                df.to_csv(outfile, sep='\t', index_label='reference')
                self.params['output'].append({
                    'sample_name': sample_name,
                    'RC': outfile,
                    'unaligned': unaligned_file,
                })
  
    def analyze_samfile(self, sam_file, unaligned_file):
        '''
        count reads
        collect unaligned files
        '''
        rc = {}
        with open(unaligned_file, 'w') as f:
            infile = pysam.AlignmentFile(sam_file, 'r')
            for rec in infile.fetch():
                if rec.reference_name:
                    if rec.reference_name not in rc:
                        rc[rec.reference_name] = 1
                    else:
                        rc[rec.reference_name] += 1
                else:
                    if rec.seq:
                        record = SeqRecord(
                            Seq(rec.seq),
                            id=rec.qname,
                            description='',
                        )
                        SeqIO.write(record, f, 'fasta')
        return rc

