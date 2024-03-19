'''
prepare commands used by external tools
'''

# Note: 
# args: the object input_data would be updated.
class ProcessCMD:
    
    @staticmethod
    def test():
        pass

    @staticmethod
    def aligner_build_index(tool, input_data:dict):
        '''
        aligner: hisat2, bowtie2 etc.
        '''
        cmd = [
            tool.exe_path,
            input_data['fa_path'],
            input_data['index_path'],
        ]
        input_data['cmd'] = ' '.join(cmd)
        return cmd

    @staticmethod
    def bowtie2_align(tool, input_data:dict):
        cmd = [
            tool.exe_path,
            '-x', input_data['index_path'],
        ]
        if input_data.get('R1') and input_data.get('R2'):
            cmd += [
                '-1', ','.join(input_data['R1']),
                '-2', ','.join(input_data['R2']),
            ]
        elif input_data.get('bam'):
            cmd += ['-b', input_data['bam']]
        elif input_data.get('unaligned'):
            cmd += ['-f', input_data['unaligned']]
        else:
            raw_data = input_data.get('R1', []) + input_data.get('R2', [])
            cmd += ['-U', ','.join(raw_data)]

        sam_file = input_data['output_prefix'] + '.sam'
        cmd += ['-S', sam_file]

        input_data.update({
            'cmd': ' '.join(cmd),
            'sam_file': sam_file,
        })
        return cmd
