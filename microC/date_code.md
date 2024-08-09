**24-08-06 scMicroC qc**
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc

python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 Bio-scMicro-C-K562_R1_001.fastq.gz -f2 Bio-scMicro-C-K562_R2_001.fastq.gz -o ./Bio-scMicro-C-K562
python /mnt/hpc/home/xuxinran/microC/trim_index.py -a CTGTCTCTTATACA -f1 Bio-scMicro-C-K562_trim_1.fq -f2 Bio-scMicro-C-K562_trim_2.fq -o ./Bio-scMicro-C-K562

seqkit stat Bio-scMicro-C-K562_R1_001.fastq.gz  Bio-scMicro-C-K562_trim_1.fq  Bio-scMicro-C-K562_trim_index_1.fq

bwa mem -5SP -T0 -t100 /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa Bio-scMicro-C-K562_trim_index_1.fq Bio-scMicro-C-K562_trim_index_2.fq -o Bio-scMicro-C-K562_aligned.sam
pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 100 --nproc-out 100 --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes Bio-scMicro-C-K562_aligned.sam > Bio-scMicro-C-K562_parsed.pairsam
pairtools sort --tmpdir ./tmp --nproc 100 Bio-scMicro-C-K562_parsed.pairsam > Bio-scMicro-C-K562_sorted.pairsam
pairtools dedup --nproc-in 100 --nproc-out 100 --mark-dups --max-mismatch 3 --backend cython --output-stats Bio-scMicro-C-K562_stats.txt --output Bio-scMicro-C-K562_dedup.pairsam Bio-scMicro-C-K562_sorted.pairsam
python3 /mnt/hpc/home/xuxinran/microC/Micro-C-main/get_qc.py -p Bio-scMicro-C-K562_stats.txt > Bio-scMicro-C-K562_qc.txt
```

**24-08-06 5次scMicroC比较**
1. clean read 汇总
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 B_L003_R1_001.fastq.gz -f2 B_L003_R2_001.fastq.gz -o ./B_L003
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 B_L003_trim_1.fq -f2 B_L003_trim_2.fq -a CTGTCTCTTATACA -o ./B_L003
cd /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 C_L003_R1_001.fastq.gz -f2 C_L003_R2_001.fastq.gz -o ./C_L003
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 C_L003_trim_1.fq -f2 C_L003_trim_2.fq -a CTGTCTCTTATACA -o ./C_L003

cd /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 scMicro-ATAC-2x_S4_L001_R1_001.fastq.gz -f2 scMicro-ATAC-2x_S4_L001_R3_001.fastq.gz -o ./scMicro-ATAC-2x
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 scMicro-ATAC-2x_trim_1.fq -f2 scMicro-ATAC-2x_trim_2.fq -a CTGTCTCTTATACA -o ./scMicro-ATAC-2x
cd /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 scMicro-ATAC-12x_S8_L001_R1_001.fastq.gz -f2 scMicro-ATAC-12x_S8_L001_R3_001.fastq.gz -o ./scMicro-ATAC-12x
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 scMicro-ATAC-12x_trim_1.fq -f2 scMicro-ATAC-12x_trim_2.fq -a CTGTCTCTTATACA -o ./scMicro-ATAC-12x


seqkit stat /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x/scMicro-ATAC-2x_S4_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x/scMicro-ATAC-2x_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x/scMicro-ATAC-2x_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x/scMicro-ATAC-12x_S8_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x/scMicro-ATAC-12x_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x/scMicro-ATAC-12x_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B/B_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B/B_L003_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B/B_L003_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C/C_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C/C_L003_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C/C_L003_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0724/scMicroC/clean_data/Bio-scMicro-C-K562_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0724/scMicroC/clean_data/Bio-scMicro-C-K562_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0724/scMicroC/clean_data/Bio-scMicro-C-K562_trim_read1N_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc/qc/2-Bio-scMicro-C-K562_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc/qc/2-Bio-scMicro-C-K562_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc/qc/2-Bio-scMicro-C-K562_trim_index_1.fq
```