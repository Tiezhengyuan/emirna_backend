'''
initialize models
example:
    python3 erna/manage.py shell < erna/scripts/init_erna.py
'''
from rna_seq.models import Method, Tool, MethodTool, \
    MethodRelation, Pipeline, Project

steps = "6".split('-')
start, end = int(steps[0]), int(steps[-1])

print('\n\n###Begin to refresh/update database###\n\n')

for enter in range(start, end+1):
    if enter == 1:
        print('Refresh Method...')
        methods = Method.objects.refresh()

    if enter == 2:
        print('Refresh Tool...')
        tools = Tool.objects.refresh()

    if enter == 3:
        print('refresh MethodTool...')
        method_tools = MethodTool.objects.refresh()

    if enter == 4:
        print('refresh MethodRelation...')
        method_relations = MethodRelation.objects.refresh()

    # TODO: confirm function
    if enter == 5:
        print('import default pipelines of miRNA-Seq...')
        mirna_seq = [
            ("build_index", 'bowtie2-build', None),
            ("trim_sequences", None, None),
            ("align_short_reads", "bowtie2", None),
            ("count_reads", None, None),
        ]
        Pipeline.objects.filter(pipeline_name='miRNA-Seq').delete()
        steps = Pipeline.objects.load_pipeline('miRNA-Seq', mirna_seq)
    
    if enter == 6:
        print("Unlock all locked projects")
        Project.objects.filter(status='locked').update(status='ready')

