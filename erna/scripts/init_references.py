'''
initialize models

example:
    python3 erna/manage.py shell < erna/scripts/init_references.py

Note:
- init_references.py covers download_references.py
'''
from rna_seq.models import Genome, AlignerIndex
from pipelines.process_genome import ProcessGenome
from pipelines.process_ncrna import ProcessNCRNA

print('\n\n###Begin to refresh/update database###\n\n')

# overwritten is False in default
# update db.Genome and db.Annotation
pg = ProcessGenome('NCBI', False)
# specie
print('Initialize db.Specie and db.Genome...')
groups = ['vertebrate_mammalian',]
species = pg.ncbi_assembly_summary(groups)

print("Download human genome from NCBI...")
pg.load_genome('Homo_sapiens', 'GCF_000001405.40')
print('Retrieve and load annotations according to molecular type...')
pg.molecular_annotation()

print('Refresh model Genome...')
genomes = Genome.objects.refresh()

# non-coding RNA
# in default: overriten is False and database is always updated.
nc = ProcessNCRNA(False)

print('Process miRNA for model RNA...')
nc.load_mirna('miRNA_hairpin')
nc.load_mirna('miRNA_mature')

print('Process long non-coding RNA for model RNA...')
nc.load_lncrna()

print('Process piwiRNA for model RNA...')
nc.load_piwirna()

print('Process rRNA for model RNA...')
nc.load_rrna()

print('Process tRNA for model RNA...')
nc.load_trna()

print('Refresh model AlignerIndex...')
AlignerIndex.objects.refresh()
