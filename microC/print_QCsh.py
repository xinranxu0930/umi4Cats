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
    parser.add_argument("--methods", choices=["MicroRUN", "MicroC", "loop"], required=True, help="选择方法: MicroRUN 或 MicroC")
    args = parser.parse_args()

    # 定义要写入文件的字符
    commands1 = f"""
    bwa mem -5SP -T0 -t{args.threads} /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa {args.read1} {args.read2} -o {args.pre}_aligned.sam
    pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in {args.threads} --nproc-out {args.threads} --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes {args.pre}_aligned.sam > {args.pre}_parsed.pairsam
    pairtools sort --tmpdir ./tmp --nproc {args.threads} {args.pre}_parsed.pairsam > {args.pre}_sorted.pairsam
    pairtools dedup --nproc-in {args.threads} --nproc-out {args.threads} --mark-dups --max-mismatch 3 --backend cython --output-stats {args.pre}_stats.txt --output {args.pre}_dedup.pairsam {args.pre}_sorted.pairsam
    python3 /mnt/hpc/home/xuxinran/microC/Micro-C-main/get_qc.py -p {args.pre}_stats.txt > {args.pre}_qc.txt
    """

    commands2 = f"""
    bwa mem -5SP -T0 -t{args.threads} /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa {args.read1} {args.read2} -o {args.pre}_aligned.sam
    pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in {args.threads} --nproc-out {args.threads} --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes {args.pre}_aligned.sam > {args.pre}_parsed.pairsam
    pairtools sort --tmpdir ./tmp --nproc {args.threads} {args.pre}_parsed.pairsam > {args.pre}_sorted.pairsam
    pairtools dedup --nproc-in {args.threads} --nproc-out {args.threads} --mark-dups --max-mismatch 3 --backend cython --output-stats {args.pre}_stats.txt --output {args.pre}_dedup.pairsam {args.pre}_sorted.pairsam
    python3 /mnt/hpc/home/xuxinran/microC/Micro-C-main/get_qc.py -p {args.pre}_stats.txt > {args.pre}_qc.txt
    pairtools split --nproc-in 50 --nproc-out 50 --output-pairs {args.pre}_mapped.pairs --output-sam {args.pre}_unsorted.bam {args.pre}_dedup.pairsam
    samtools sort -@{args.threads} -o {args.pre}_mapped.bam {args.pre}_unsorted.bam
    samtools index -@{args.threads} {args.pre}_mapped.bam
    grep -v '#' {args.pre}_mapped.pairs | awk -F"\\t" '{{print $1"\\t"$2"\\t"$3"\\t"$6"\\t"$4"\\t"$5"\\t"$7}}' | gzip -c > {args.pre}_mapped.pairs.gz
    samtools view -@ {args.threads} -h -F 0x900 {args.pre}_mapped.bam | bedtools bamtobed -i stdin > {args.pre}.primary.aln.bed
    macs2 callpeak -t {args.pre}.primary.aln.bed -n {args.pre}.macs2
    samtools view -h {args.pre}_mapped.bam | grep -v '^chrM' | samtools view -b -o {args.pre}_mapped_f.bam
    samtools index {args.pre}_mapped_f.bam
    grep -v '^chrM' {args.pre}.macs2_peaks.narrowPeak > {args.pre}.macs2_peaks_f.narrowPeak
    rm {args.pre}_mapped.bam* {args.pre}.macs2_peaks.narrowPeak
    bash /mnt/hpc/home/xuxinran/microC/HiChiP/enrichment_stats.sh -g /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -b {args.pre}_mapped_f.bam -p {args.pre}.macs2_peaks_f.narrowPeak -x {args.pre}
    """

    commands3 = f"""
    bwa mem -5SP -T0 -t{args.threads} /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa {args.read1} {args.read2} -o {args.pre}_aligned.sam
    pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in {args.threads} --nproc-out {args.threads} --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes {args.pre}_aligned.sam > {args.pre}_parsed.pairsam
    pairtools sort --tmpdir ./tmp --nproc {args.threads} {args.pre}_parsed.pairsam > {args.pre}_sorted.pairsam
    pairtools dedup --nproc-in {args.threads} --nproc-out {args.threads} --mark-dups --max-mismatch 3 --backend cython --output-stats {args.pre}_stats.txt --output {args.pre}_dedup.pairsam {args.pre}_sorted.pairsam
    python3 /mnt/hpc/home/xuxinran/microC/Micro-C-main/get_qc.py -p {args.pre}_stats.txt > {args.pre}_qc.txt
    pairtools split --nproc-in 50 --nproc-out 50 --output-pairs {args.pre}_mapped.pairs --output-sam {args.pre}_unsorted.bam {args.pre}_dedup.pairsam
    java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads {args.threads} {args.pre}_mapped.pairs {args.pre}_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
    java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads {args.threads} -r 5000,10000 --ignore-sparsity {args.pre}_contact_map.hic {args.pre}_hic.hiccups
    """

    if args.methods == "MicroRUN":
        commands = "\n".join(line.strip() for line in commands2.strip().split("\n"))
    elif args.methods == "loop":
        commands = "\n".join(line.strip() for line in commands3.strip().split("\n"))
    else:
        commands = "\n".join(line.strip() for line in commands1.strip().split("\n"))

    # 指定文件路径
    if args.tmp:
        call(f"mkdir {args.outdir}/tmp", shell=True)

    file_path = f"{args.pre}_run.sh"

    # 将字符写入文件
    with open(file_path, "w") as file:
        file.write(commands)

    print(f"Commands have been written to {file_path}")