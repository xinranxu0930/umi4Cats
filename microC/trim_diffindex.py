import mappy as mp
import argparse
import re

def trim(sample, fq1, fq2, primer_match_len=6):
    total = 0
    with_primer, without_primer = 0, 0
    yes_insert, no_insert = 0, 0
    trim_fq1_name = f"{sample}_trim_1.fq"
    trim_fq2_name = f"{sample}_trim_2.fq"
    trim_fq1 = open(trim_fq1_name, "w")
    trim_fq2 = open(trim_fq2_name, "w")

    for read1, read2 in zip(
        mp.fastx_read(fq1, read_comment=True),
        mp.fastx_read(fq2, read_comment=True),
    ):
        total += 1
        read_name, comment = read1[0], read1[-1][1:]
        seq1, qual1 = read1[1], read1[2]
        seq2, qual2 = read2[1], read2[2]

        # Extract the adapter from the comment
        adapter = comment.split(":")[-1].strip()
        if "+" in adapter:
            adapter = adapter.split("+")[0]
        if adapter.startswith("N"):
            three_primer = adapter[1:]
        else:
            three_primer = adapter

        if three_primer in seq1:
            with_primer += 1
            if seq1.startswith(three_primer):
                no_insert += 1
                continue
            else:
                yes_insert += 1
                insert_len = len(seq1.split(three_primer)[0])
        else:
            without_primer += 1
            insert_len = 150
        if len(qual1[:insert_len])<60 or len(qual2[:insert_len])<60:
            continue
        trim_fq1.write(f"@{read_name} 1{comment}\n{seq1[:insert_len]}\n+\n{qual1[:insert_len]}\n")
        trim_fq2.write(f"@{read_name} 2{comment}\n{seq2[:insert_len]}\n+\n{qual2[:insert_len]}\n")
    trim_fq1.close()
    trim_fq2.close()

    trim_count = {
        "total": total,
        "with_primer": with_primer,
        "without_primer": without_primer,
        "yes_insert": yes_insert,
        "no_insert": no_insert,
    }
    print(f"Trim results: {trim_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check microC fastq adapter.')
    parser.add_argument("-f1","--fastq1", type=str, help="R1 fastq file path")
    parser.add_argument("-f2","--fastq2", type=str, help="R2 fastq file path")
    parser.add_argument("-o","--output_pre", type=str, help="output prefix")
    args = parser.parse_args()

    trim(args.output_pre, args.fastq1, args.fastq2)
