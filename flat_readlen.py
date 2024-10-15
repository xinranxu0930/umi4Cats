import mappy as mp
import argparse


def get_splitread(sample_name, fq1, fq2, max_len):
    split_fq1_name = f"{sample_name}_R1.fq"
    split_fq2_name = f"{sample_name}_R2.fq"
    split_fq1 = open(split_fq1_name, "w")
    split_fq2 = open(split_fq2_name, "w")

    for read1, read2 in zip(
        mp.fastx_read(fq1, read_comment=True),
        mp.fastx_read(fq2, read_comment=True),
    ):
        read_name, comment = read1[0], read1[-1][1:]
        seq1, qual1 = read1[1], read1[2]
        seq2, qual2 = read2[1], read2[2]

        split_fq1.write(f"@{read_name} 1{comment}\n{seq1[:max_len]}\n+\n{qual1[:max_len]}\n")
        split_fq2.write(f"@{read_name} 2{comment}\n{seq2[:max_len]}\n+\n{qual2[:max_len]}\n")
    split_fq1.close()
    split_fq2.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GET valid uni4C fastq.')
    parser.add_argument("-f1","--fastq1", type=str, help="R1 fastq file path")
    parser.add_argument("-f2","--fastq2", type=str, help="R2 fastq file path")
    parser.add_argument("-m","--max_len", type=int, help="read max length")
    args = parser.parse_args()

    sample_name = args.fastq1.split("_tmp")[0]

    get_splitread(sample_name, args.fastq1, args.fastq2, args.max_len)