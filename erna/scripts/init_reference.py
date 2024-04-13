'''
initialize models
example:
    python3 erna/manage.py shell < erna/scripts/init_reference.py
'''
from rna_seq.models import Genome, AlignerIndex
from pipelines.process_genome import ProcessGenome
from pipelines.process_ncrna import ProcessNCRNA

print('\n\n###Begin to refresh/update database###\n\n')

start_end = '1-11'.split('-')
start, end = int(start_end[0]), int(start_end[-1])
for enter in range(start, end + 1):
    match enter:
        # specie
        case 1:
            print('Initialize db.Specie and db.Genome...')
            species = ProcessGenome('NCBI').ncbi_assembly_summary(['vertebrate_mammalian',])
        case 2:
            print("Download human genome from NCBI...")
            # update db.Genome and db.Annotation
            ProcessGenome('NCBI', 'Homo_sapiens', 'GCF_000001405.40').download_genome()
        case 4:
            print('Retrieve and load annotations according to molecular type...')
            ProcessGenome('NCBI', 'Homo_sapiens', 'GCF_000001405.40', False).molecular_annotation()
        case 5:
            print('Refresh model Genome...')
            genomes = Genome.objects.refresh()

        # non-coding RNA
        case 6:
            print('Process miRNA for model RNA...')
            ProcessNCRNA().load_mirna('miRNA_hairpin')
            ProcessNCRNA().load_mirna('miRNA_mature')
        case 7:
            print('Process long non-coding RNA for model RNA...')
            ProcessNCRNA().load_lncrna()
        case 8:
            print('Process piwiRNA for model RNA...')
            ProcessNCRNA().load_piwirna()
        case 9:
            print('Process rRNA for model RNA...')
            ProcessNCRNA().load_rrna()
        case 10:
            print('Process tRNA for model RNA...')
            ProcessNCRNA().load_trna()

        case 11:
            print('Refresh model AlignerIndex...')
            AlignerIndex.objects.refresh()
