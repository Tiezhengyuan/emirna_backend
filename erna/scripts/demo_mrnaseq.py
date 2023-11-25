'''
example:
    python3 erna/manage.py shell < erna/scripts/demo_project.py
'''
import json
from rna_seq.models import *
from commons.models import CustomUser


user = CustomUser.objects.get(pk=1)
specie_name = 'Homo_sapiens'
genome = Genome.objects.get_genome(specie_name, 'GCF_000001405.40')
project_id = "P00001"

# cretae project
new_project = {
    "project_id": project_id,
    "project_name": "test_mrna_seq",
    "description": "for testing mRNA-seq",
    "status": "A",
    "sequencing": "M",
    'owner': user,
    'genome': genome,
}
Project.objects.filter(project_id=project_id).delete()
project = Project.objects.create(**new_project)
print(project)

# add tasks
tasks_data = [
    {
        'task_id': 'T01',
        'method_name': 'build_index',
        'tool': {
            'tool_name': 'hisat2',
            'exe_name': 'hisat2-build',
            'version': '2.2.1',
        },
        'params': {},
        'genome':{
            'data_source': 'NCBI',
            'specie': specie_name,
            'version': 'GCF_000001405.40',
        },
        'annotation':{
            "file_format": "fna",
            "annot_type": "genomic",
        },
        'child': ['T02'],
    },
    {
        'task_id': 'T02',
        'task_name': '',
        'method_name': 'align_transcriptome',
        'tool': {
            'tool_name': 'hisat2',
            'exe_name': 'hisat2',
            'version': '2.2.1',
        },
        'child': ['T03'],
    },
    {
        'task_id': 'T03',
        'task_name': '',
        'method_name': 'convert_format',
        'tool': {
            'tool_name': 'samtools',
            'exe_name': 'samtools',
            'version': '1.18',
        },
        'params': {},
        'child': ['T04'],
    },
    {
        'task_id': 'T04',
        'task_name': '',
        'method_name': 'assemble_transcripts',
        'tool': {
            'tool_name': 'stringtie',
            'exe_name': 'stringtie',
            'version': '2.2.2',
        },
        'params': {},
        'child': ['T05', 'T06'],
    },
    {
        'task_id': 'T05',
        'task_name': '',
        'method_name': 'merge_transcripts',
        'tool': {
            'tool_name': 'stringtie',
            'exe_name': 'stringtie',
            'version': '2.2.2',
        },
        'params': {},
    },
    {
        'task_id': 'T06',
        'task_name': '',
        'method_name': 'count_reads',
        'parent': ['T04'],
    },
    {
        'task_id': 'T07',
        'task_name': '',
        'method_name': 'quality_control',
        'tool': {
            "tool_name": "fastqc",
            "exe_name": "fastqc",
            'version': '0.12.1'
        }
    },
]
tasks = Task.objects.load_tasks(project_id, tasks_data)
print(tasks)

tasks_tree = TaskTree.objects.load_tasks_tree(project_id, tasks_data)
print(tasks_tree)


# load samples
study_name = 'test_mrnaseq'
sample_names = ['197_L1', '1014_L1', '1073_L1']
sample_data = [{'study_name':study_name, 'sample_name':s, 'metadata':{},} \
    for s in sample_names]
samples = Sample.objects.load_samples(user, sample_data)
print(samples)

#RawData
batch_names = ['demo_mrnaseq',]
sample_files = SampleFile.objects.parse_sample_rawdata([study_name,], batch_names)

# update SampleProject
res = SampleProject.objects.load_project_sample_files(
    project_id, [s.id for s,_ in sample_files]
)
print(res)