import mappy as mp
import argparse


def get_viewpoint(
    sample, fq1, fq2, viewpoint_seq, enz_seq, viewpoint_name, replication_name, min_len
):
    viewpoint_fq1_name = f"{sample}_{replication_name}_{viewpoint_name}_tmp_R1.fq"
    viewpoint_fq2_name = f"{sample}_{replication_name}_{viewpoint_name}_tmp_R2.fq"
    viewpoint_fq1 = open(viewpoint_fq1_name, "w")
    viewpoint_fq2 = open(viewpoint_fq2_name, "w")

    required_seq = viewpoint_seq + enz_seq
    total_reads, valid_reads, unvalid_reads = 0, 0, 0

    for read1, read2 in zip(
        mp.fastx_read(fq1, read_comment=True),
        mp.fastx_read(fq2, read_comment=True),
    ):
        total_reads += 1
        if read1[-1] != None:
            comment = read1[-1][1:]
        else:
            comment = ""
        read_name = read1[0]
        seq1, qual1 = read1[1], read1[2]
        seq2, qual2 = read2[1], read2[2]
        # 2种计数： required_seq存在（有效） required_seq不在（无效）
        # 只处理read1 read2不用管
        if required_seq in seq1:
            if not seq1.startswith(required_seq):
                unvalid_len = len(seq1.split(required_seq)[0])
                if unvalid_len > (150 - min_len):
                    unvalid_reads += 1
                    continue
                else:
                    viewpoint_fq1.write(f"@{read_name} 1{comment}\n{seq1[unvalid_len:]}\n+\n{qual1[unvalid_len:]}\n")
                    viewpoint_fq2.write(f"@{read_name} 2{comment}\n{seq2}\n+\n{qual2}\n")
                    valid_reads += 1
            else:
                viewpoint_fq1.write(f"@{read_name} 1{comment}\n{seq1}\n+\n{qual1}\n")
                viewpoint_fq2.write(f"@{read_name} 2{comment}\n{seq2}\n+\n{qual2}\n")
                valid_reads += 1
        else:
            unvalid_reads += 1
    viewpoint_fq1.close()
    viewpoint_fq2.close()
    viewpoint_count = {
        "sample": sample,
        "total": total_reads,
        "valid reads number": valid_reads,
        "valid reads ratio": f"{100*valid_reads/total_reads:.2f}%",
        "unvalid reads number": unvalid_reads,
        "unvalid reads ratio": f"{100*unvalid_reads/total_reads:.2f}%",
    }
    print(viewpoint_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GET valid uni4C fastq.")
    parser.add_argument("-f1", "--fastq1", type=str, help="R1 fastq file path")
    parser.add_argument("-f2", "--fastq2", type=str, help="R2 fastq file path")
    parser.add_argument("-v", "--viewpoint", type=str, help="viewpoint sequence")
    parser.add_argument("-e", "--enzyme", type=str, help="enzyme sequence")
    parser.add_argument("-n", "--viewpoint_name", type=str, help="viewpoint name")
    parser.add_argument(
        "-r", "--replication_name", type=str, help="replication name", default="1"
    )
    parser.add_argument("-o", "--output_pre", type=str, help="output prefix")
    parser.add_argument("-m", "--min_len", type=int, help="read min length", default=50)
    args = parser.parse_args()

    get_viewpoint(
        args.output_pre,
        args.fastq1,
        args.fastq2,
        args.viewpoint,
        args.enzyme,
        args.viewpoint_name,
        args.replication_name,
        args.min_len,
    )

    # seqkit看一下所有带分析的fastq中最短的序列长度，和这个持平
