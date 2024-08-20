import argparse
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='8 Kinds of Nanopore Direct RNA QTL Colocalization.')
    parser.add_argument("-o", "--outdir", type=str, help="output directory")
    parser.add_argument("-p", "--pre", type=str, default=0.05, help="output dir and prefix")
    parser.add_argument("-1", "--read1", type=str, help="read1 file path")
    parser.add_argument("-2", "--read2", type=str, help="read2 file path")
    parser.add_argument("-t", "--threads", type=int, default=20, help="threads num(default=20)")
    parser.add_argument("--tmp", action='store_true', help="是否需要创建tmp文件夹")

    args = parser.parse_args()

    # 定义要写入文件的字符
    commands = f"""
    bwa mem -5SP -T0 -t{args.threads} /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa {args.read1} {args.read2} -o {args.pre}_aligned.sam
    pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in {args.threads} --nproc-out {args.threads} --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes {args.pre}_aligned.sam > {args.pre}_parsed.pairsam
    pairtools sort --tmpdir ./tmp --nproc {args.threads} {args.pre}_parsed.pairsam > {args.pre}_sorted.pairsam
    pairtools dedup --nproc-in {args.threads} --nproc-out {args.threads} --mark-dups --max-mismatch 3 --backend cython --output-stats {args.pre}_stats.txt --output {args.pre}_dedup.pairsam {args.pre}_sorted.pairsam
    python3 /mnt/hpc/home/xuxinran/microC/Micro-C-main/get_qc.py -p {args.pre}_stats.txt > {args.pre}_qc.txt
    """
    commands = "\n".join(line.strip() for line in commands.strip().split("\n"))

    # 指定文件路径
    if args.tmp:
        call(f"mkdir {args.outdir}/tmp", shell=True)

    file_path = f"{args.pre}_run.sh"

    # 将字符写入文件
    with open(file_path, "w") as file:
        file.write(commands)

    print(f"Commands have been written to {file_path}")