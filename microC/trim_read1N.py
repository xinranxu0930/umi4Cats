import mappy as mp
import argparse

def trim(sample, fq1, fq2, index_seq):
    trim_fq1_name = f"{sample}_trim_adapter_1.fq"
    trim_fq2_name = f"{sample}_trim_adapter_2.fq"
    trim_fq1 = open(trim_fq1_name, "w")
    trim_fq2 = open(trim_fq2_name, "w")
    for read1, read2 in zip(
        mp.fastx_read(fq1, read_comment=True),
        mp.fastx_read(fq2, read_comment=True),
    ):
        read_name, comment = read1[0], read1[-1][1:]
        seq1, qual1 = read1[1], read1[2]
        seq2, qual2 = read2[1], read2[2]

        insert_len = 0
        sub_seq = index_seq[-8:]
        if sub_seq in seq1:
            insert_len = len(seq1.split(sub_seq)[-1])
            if insert_len < 60:
                continue
        trim_fq1.write(f"@{read_name} 1{comment}\n{seq1[-insert_len:]}\n+\n{qual1[-insert_len:]}\n")
        trim_fq2.write(f"@{read_name} 2{comment}\n{seq2[-insert_len:]}\n+\n{qual2[-insert_len:]}\n")
    trim_fq1.close()
    trim_fq2.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check microC fastq adapter.')
    parser.add_argument("-f1","--fastq1", type=str, help="R1 fastq file path")
    parser.add_argument("-f2","--fastq2", type=str, help="R2 fastq file path")
    parser.add_argument("-a","--adapter", type=str, help="adapter sequence(must more than 10bp)")
    parser.add_argument("-o","--output_pre", type=str, help="output prefix")
    args = parser.parse_args()

    trim(args.output_pre, args.fastq1, args.fastq2, args.adapter)