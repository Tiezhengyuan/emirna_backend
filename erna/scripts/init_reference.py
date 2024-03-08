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
        # genome
        case 1:
            print('Initialize db.Specie and db.Genome...')
            species = ProcessGenome('NCBI').ncbi_assembly_summary(['vertebrate_mammalian',])
        case 2:
            print("Download human genome from NCBI...")
            # update db.Genome and db.Annotation
            ProcessGenome('NCBI', 'Homo_sapiens', 'GCF_000001405.40').download_genome()
            # ProcessGenome('NCBI', 'Homo_sapiens', 'GCF_009914755.1').download_genome()
        case 3:
            print("Download other genome from NCBI...")
            # update db.Genome and db.Annotation
            ProcessGenome('NCBI', 'Ailuropoda_melanoleuca', 'GCF_002007445.2').download_genome()
        case 4:
            print('Retrieve and load annotations according to molecular type...')
            ProcessGenome('NCBI', 'Homo_sapiens', 'GCF_000001405.40', False).molecular_annotation()
            # ProcessGenome('NCBI', 'Homo_sapiens', 'GCF_009914755.1', False).molecular_annotation()
        case 5:
            print('Refresh model Genome...')
            genomes = Genome.objects.refresh()
        case 6:
            print('Refresh model AlignerIndex...')
            AlignerIndex.objects.refresh()

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


