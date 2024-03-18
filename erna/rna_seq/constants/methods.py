ROOT_METHOD = {
  "method_name": "import_data",
  "description": "bound with task T00",
}

GENERAL_METHODS = [
  {
    "method_name": "trim_sequences",
    "description": "miRNA-seq",
    "child_method": ["align_short_reads",],
    "exe_name": [],
    "default_params": {'adapter_3end': 'TGGAATTCTCGGGTGCCAAGG',},
  },
  {
    "method_name": "align_short_reads",
    "description": "",
    "child_method": ["count_reads", "convert_format",],
    "exe_name": ["bowtie2",],
  },
  {
    "method_name": "build_index",
    "description": "build index for sequencing alignment",
    "child_method": ["align_short_reads",],
    "exe_name": ["bowtie2-build",],
  },
  {
    "method_name": "count_reads",
    "description": "count reads and collect unaligned reads",
    "child_method": ["merge_read_counts", "align_short_reads",],
    "exe_name": [],
  },
  {
    "method_name": "merge_read_counts",
    "description": "count reads for differential expression",
    "child_method": [],
    "exe_name": [],
  },
  {
    "method_name": "quality_control",
    "description": "sequencing quality control",
    "child_method": [],
    "exe_name": ["fastqc"],
  },
  {
    "method_name": "convert_format",
    "description": "sam-bam",
    "child_method": [],
    "exe_name": ["samtools"],
  },
]

METHODS = [ROOT_METHOD, ] + GENERAL_METHODS