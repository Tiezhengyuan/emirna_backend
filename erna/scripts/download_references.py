'''
download omics data from public database

example:
    export REFERENCES_DIR=/home/yuan/bio/emirna_backend/references
    python3 erna/scripts/download_references.py

Note: 
- in default, overriten is False
- configuration should be consistent with init_reference.py
- omics data might be covered by init_references.py
'''
import os
from bioomics import NCBI, Mirbase, RNACentral
from biosequtils import HandleJson


print('\n\n###Begin to download omics data.###\n\n')
ref_dir = os.environ.get('REFERENCES_DIR')
overwrite=False

start_end = '1-5'.split('-')
start, end = int(start_end[0]), int(start_end[-1])
for enter in range(start, end + 1):
    match enter:
        # specie genome from NCBI
        case 1:
            print("Download human genome from NCBI...")
            conn = NCBI(ref_dir, overwrite)

            # download assembly_summary.txt
            groups = ['vertebrate_mammalian',]
            output_dir, text_files = conn.download_assembly_summary(groups)
            for text_file in text_files.values():
                # convert txt to json
                json_file = HandleJson(text_file).from_text()
                obj_iter = HandleJson(json_file).read_json()
                # download genome
                for _, summary in obj_iter:
                    if summary["organism_name"] == "Homo sapiens":
                        conn.download_genome(summary['ftp_path'], \
                            'Homo_sapiens', 'GCF_000001405.40')
        
        # miRNA   
        case 2:
            print('Process miRNA for model RNA...')
            conn = Mirbase(ref_dir, overwrite)
            conn.download_hairpin()
            conn.download_mature()
        
        # non-coding RNA
        case 3:
            conn = RNACentral(ref_dir, overwrite)
            
            print('Process long non-coding RNA for model RNA...')
            conn.download_sequence('lncbook.fasta')
            
            print('Process piwiRNA for model RNA...')
            conn.download_sequence('pirbase.fasta')
            
            print('Process rRNA for model RNA...')
            conn.download_sequence('5srrnadb.fasta')
            
            print('Process tRNA for model RNA...')
            conn.download_sequence('gtrnadb.fasta')
