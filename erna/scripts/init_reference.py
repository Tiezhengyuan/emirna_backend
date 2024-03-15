'''
initialize models
example:
    python3 erna/manage.py shell < erna/scripts/init_reference.py
'''
from rna_seq.models import Genome, AlignerIndex
from pipelines.process.process_genome import ProcessGenome
from pipelines.process.process_ncrna import ProcessNCRNA

print('\n\n###Begin to refresh/update database###\n\n')

start_end = '6'.split('-')
start, end = int(start_end[0]), int(start_end[-1])
for enter in range(start, end + 1):
    match enter:
        # specie
        case 1:
            print('Initialize db.Specie and db.Genome...')
            species = ProcessGenome('NCBI').ncbi_assembly_summary(['vertebrate_mammalian',])
        # non-coding RNA
        case 11:
            print('Process miRNA for model RNA...')
            ProcessNCRNA().load_mirna('miRNA_hairpin')
            ProcessNCRNA().load_mirna('miRNA_mature')
        case 12:
            print('Process long non-coding RNA for model RNA...')
            ProcessNCRNA().load_lncrna()
        case 13:
            print('Process piwiRNA for model RNA...')
            ProcessNCRNA().load_piwirna()
        case 14:
            print('Process rRNA for model RNA...')
            ProcessNCRNA().load_rrna()
        case 15:
            print('Process tRNA for model RNA...')
            ProcessNCRNA().load_trna()


