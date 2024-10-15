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

**24-08-20 MicroCRUN**
```shell
# 去index
## no生物素
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-CTCF-2_L7_G007 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-K27ac-2_L7_G028 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-4_L7_G092.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-4_L7_G092.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-CTCF-4_L7_G092 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-4_L7_G027.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-4_L7_G027.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-K27ac-4_L7_G027 -i GATCGGAAGAGCA
## 生物素
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-2_L4_G029.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-2_L4_G029.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-CTCF-2_L4_G029 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-CTCF-4_L4_G042 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-K27ac-2_L4_G005 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-4_L4_G084.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-4_L4_G084.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-K27ac-4_L4_G084 -i GATCGGAAGAGCA

# 去adapter
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-CTCF-2_L4_G029_trim_index_1.fq -f2 bio-GM-CTCF-2_L4_G029_trim_index_2.fq -o bio-GM-CTCF-2_L4_G029 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-CTCF-4_L4_G042_trim_index_1.fq -f2 bio-GM-CTCF-4_L4_G042_trim_index_2.fq -o bio-GM-CTCF-4_L4_G042 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-K27ac-2_L4_G005_trim_index_1.fq -f2 bio-GM-K27ac-2_L4_G005_trim_index_2.fq -o bio-GM-K27ac-2_L4_G005 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-K27ac-4_L4_G084_trim_index_1.fq -f2 bio-GM-K27ac-4_L4_G084_trim_index_2.fq -o bio-GM-K27ac-4_L4_G084 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-CTCF-2_L7_G007_trim_index_1.fq -f2 no-GM-CTCF-2_L7_G007_trim_index_2.fq -o no-GM-CTCF-2_L7_G007 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-CTCF-4_L7_G092_trim_index_1.fq -f2 no-GM-CTCF-4_L7_G092_trim_index_2.fq -o no-GM-CTCF-4_L7_G092 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-K27ac-2_L7_G028_trim_index_1.fq -f2 no-GM-K27ac-2_L7_G028_trim_index_2.fq -o no-GM-K27ac-2_L7_G028 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-K27ac-4_L7_G027_trim_index_1.fq -f2 no-GM-K27ac-4_L7_G027_trim_index_2.fq -o no-GM-K27ac-4_L7_G027 -a CGCTCTTCCGATCT

seqkit stat /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-2_L4_G029.R1.fastq.gz bio-GM-CTCF-2_L4_G029_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R1.fastq.gz bio-GM-CTCF-4_L4_G042_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R1.fastq.gz bio-GM-K27ac-2_L4_G005_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-4_L4_G084.R1.fastq.gz bio-GM-K27ac-4_L4_G084_trim_adapter_1.fq > bio-GM_seqkit.txt
seqkit stat /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R1.fastq.gz no-GM-CTCF-2_L7_G007_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-4_L7_G092.R1.fastq.gz no-GM-CTCF-4_L7_G092_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R1.fastq.gz no-GM-K27ac-2_L7_G028_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-4_L7_G027.R1.fastq.gz no-GM-K27ac-4_L7_G027_trim_adapter_1.fq > no-GM_seqkit.txt

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-CTCF-2_L4_G029_trim_read1N_1.fq -2 ./clean_data/bio-GM-CTCF-2_L4_G029_trim_read1N_2.fq -p ./bio-GM-CTCF-2_L4_G029
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-CTCF-4_L4_G042_trim_read1N_1.fq -2 ./clean_data/bio-GM-CTCF-4_L4_G042_trim_read1N_2.fq -p ./bio-GM-CTCF-4_L4_G042
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-K27ac-2_L4_G005_trim_read1N_1.fq -2 ./clean_data/bio-GM-K27ac-2_L4_G005_trim_read1N_2.fq -p ./bio-GM-K27ac-2_L4_G005
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-K27ac-4_L4_G084_trim_read1N_1.fq -2 ./clean_data/bio-GM-K27ac-4_L4_G084_trim_read1N_1.fq -p ./bio-GM-K27ac-4_L4_G084
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-CTCF-2_L7_G007_trim_read1N_1.fq -2 ./clean_data/no-GM-CTCF-2_L7_G007_trim_read1N_2.fq -p ./no-GM-CTCF-2_L7_G007
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-CTCF-4_L7_G092_trim_read1N_1.fq -2 ./clean_data/no-GM-CTCF-4_L7_G092_trim_read1N_2.fq -p ./no-GM-CTCF-4_L7_G092
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-K27ac-2_L7_G028_trim_read1N_1.fq -2 ./clean_data/no-GM-K27ac-2_L7_G028_trim_read1N_2.fq -p ./no-GM-K27ac-2_L7_G028

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-K27ac-4_L7_G027_trim_read1N_1.fq -2 ./clean_data/no-GM-K27ac-4_L7_G027_trim_read1N_2.fq -p ./no-GM-K27ac-4_L7_G027

## 饱和度
python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R2.fastq.gz -o bio-GM-CTCF-2_L4_G029

python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R2.fastq.gz -o ./bio-GM-K27ac-2_L4_G005
python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R2.fastq.gz -o ./no-GM-CTCF-2_L7_G007
python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R2.fastq.gz -o ./no-GM-K27ac-2_L7_G028

```

**24-08-29 MicroCRUN**
```shell
# 去index
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-CTCF-8MCUT_L3_Q0060W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-CTCF-8MCUT_L3_Q0060W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-CTCF-8MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-1MCUT_L3_Q0056W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-1MCUT_L3_Q0056W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K4me3-1MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-4MCUT_L3_Q0058W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-4MCUT_L3_Q0058W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K4me3-4MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-10MCUT_L3_Q0061W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-10MCUT_L3_Q0061W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K4me3-10MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-2MCUT_L3_Q0057W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-2MCUT_L3_Q0057W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K27ac-2MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-6MCUT_L3_Q0059W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-6MCUT_L3_Q0059W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K27ac-6MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-10MCUT_L3_Q0062W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-10MCUT_L3_Q0062W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K27ac-10MCUT -i CTGTCTCTTATACACAT

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-CTCF-8MCUT_trim_index_1.fq -2 ./clean_data/GM-CTCF-8MCUT_trim_index_2.fq -p ./GM-CTCF-8MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K27ac-10MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K27ac-10MCUT_trim_index_2.fq -p ./GM-H3K27ac-10MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K27ac-2MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K27ac-2MCUT_trim_index_2.fq -p ./GM-H3K27ac-2MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K27ac-6MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K27ac-6MCUT_trim_index_2.fq -p ./GM-H3K27ac-6MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K4me3-10MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K4me3-10MCUT_trim_index_2.fq -p ./GM-H3K4me3-10MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K4me3-1MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K4me3-1MCUT_trim_index_2.fq -p ./GM-H3K4me3-1MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K4me3-4MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K4me3-4MCUT_trim_index_2.fq -p ./GM-H3K4me3-4MCUT --methods MicroRUN

seqkit stat /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-CTCF-8MCUT_L3_Q0060W0179.R1.fastq.gz ./clean_data/GM-CTCF-8MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-1MCUT_L3_Q0056W0179.R1.fastq.gz ./clean_data/GM-H3K4me3-1MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-4MCUT_L3_Q0058W0179.R1.fastq.gz ./clean_data/GM-H3K4me3-4MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-10MCUT_L3_Q0061W0179.R1.fastq.gz ./clean_data/GM-H3K4me3-10MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-2MCUT_L3_Q0057W0179.R1.fastq.gz ./clean_data/GM-H3K27ac-2MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-6MCUT_L3_Q0059W0179.R1.fastq.gz ./clean_data/GM-H3K27ac-6MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-10MCUT_L3_Q0062W0179.R1.fastq.gz ./clean_data/GM-H3K27ac-10MCUT_trim_index_1.fq
```

**24-09-01**
```shell
# 一、rs3731239在microC的loop情况
## 


# 二、microRUN 和公共数据比较
## 1、下载数据
$prefetch -v SRR16356487 --max-size 50G # GSM5628869 HCT_GM12878_H3K27ac_Rep1
$prefetch -v SRR16356486 --max-size 50G # GSM5628870 HCT_GM12878_H3K27ac_Rep2
$prefetch -v SRR16356485 --max-size 50G # GSM5628871 HCT_GM12878_H3K27ac_Rep3
$prefetch -v SRR5831489 --max-size 50G # GSM2705041 GM HiChIP H3K27ac biological replicate 1
$prefetch -v SRR5831490 --max-size 50G # GSM2705042 GM HiChIP H3K27ac biological replicate 2
mv SRR16356487.sra HCT_GM12878_H3K27ac_Rep1.sra
mv SRR16356486.sra HCT_GM12878_H3K27ac_Rep2.sra
mv SRR16356485.sra HCT_GM12878_H3K27ac_Rep3.sra
mv SRR5831489.sra GM_HiChIP_H3K27ac_biological_replicate1.sra
mv SRR5831490.sra GM_HiChIP_H3K27ac_biological_replicate2.sra
fastq-dump --gzip --split-3 -O ./ HCT_GM12878_H3K27ac_Rep1.sra
fastq-dump --gzip --split-3 -O ./ HCT_GM12878_H3K27ac_Rep2.sra
fastq-dump --gzip --split-3 -O ./ HCT_GM12878_H3K27ac_Rep3.sra
fastq-dump --gzip --split-3 -O ./ GM_HiChIP_H3K27ac_biological_replicate1.sra
fastq-dump --gzip --split-3 -O ./ GM_HiChIP_H3K27ac_biological_replicate2.sra
cat HCT_GM12878_*_1.fastq.gz > HCT_GM12878_H3K27ac_1.fastq.gz
cat HCT_GM12878_*_2.fastq.gz > HCT_GM12878_H3K27ac_2.fastq.gz
cat GM_HiChIP_H3K27ac_biological_*_1.fastq.gz > GM_HiChIP_H3K27ac_biological_1.fastq.gz
cat GM_HiChIP_H3K27ac_biological_*_2.fastq.gz > GM_HiChIP_H3K27ac_biological_2.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-*.R1.fastq.gz > GM-H3K27ac.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-*.R2.fastq.gz > GM-H3K27ac.R2.fastq.gz

## 2、去除index
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 GM-H3K27ac.R1.fastq.gz -f2 GM-H3K27ac.R2.fastq.gz -o ./GM-H3K27ac -i CTGTCTCTTATACACAT

## 3、QC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./GM_QC -t 100 -1 ./data/GM-H3K27ac_trim_index_1.fq -2 ./data/GM-H3K27ac_trim_index_2.fq -p ./GM_QC/GM-H3K27ac --methods MicroRUN --tmp
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./HCT_QC -t 100 -1 ./data/HCT_GM12878_H3K27ac_1.fastq.gz -2 ./data/HCT_GM12878_H3K27ac_2.fastq.gz -p ./HCT_QC/HCT_GM12878_H3K27ac --methods MicroRUN --tmp
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./HiChIP_QC -t 100 -1 ./data/GM_HiChIP_H3K27ac_biological_replicate2_1.fastq.gz -2 ./data/GM_HiChIP_H3K27ac_biological_replicate2_2.fastq.gz -p ./GM_HiChIP_H3K27ac_biological --methods MicroRUN

# fithichip
export PATH="/f/xinran/MicroC/HiC-Pro_3.1.0/bin/:$PATH"
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C /f/xinran/11111/GM_fithichip/config.txt
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C /f/xinran/11111/HCT_fithichip/config.txt
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C config.txt

# loop
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 100 /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_mapped.pairs /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 100 -r 5000,10000 --ignore-sparsity /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_hic.hiccups

java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 100 /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_mapped.pairs /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 100 -r 5000,10000 --ignore-sparsity /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_hic.hiccups

java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 100 /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_mapped.pairs /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 100 -r 5000,10000 --ignore-sparsity /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_contact_map.hic /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_hic.hiccups


```

**24-09-01** 合并所有的young和old的数据 call loop、loopQTL 查看一端是promoter一端SNP的loop/valid pair
```shell
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240311/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240522_pool_microC_microCUT/old-po-Micro-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240521_LH00524_0040_A223YVLLT4/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240607_LH00308_0156_B223VFVLT4/old-po-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240611_LH00524_0057_A2253NYLT4/old-po-microc-rep5_L3_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-Micro-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240828_LH00308_0228_B22FM25LT4/old-po-microc-32/old-po-microc-32_L6_G041.R1.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/old_merge.R1.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240311/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240522_pool_microC_microCUT/old-po-Micro-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240521_LH00524_0040_A223YVLLT4/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240607_LH00308_0156_B223VFVLT4/old-po-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240611_LH00524_0057_A2253NYLT4/old-po-microc-rep5_L3_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-Micro-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240828_LH00308_0228_B22FM25LT4/old-po-microc-32/old-po-microc-32_L6_G041.R2.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/old_merge.R2.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240716_microrun_microc/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240824_LH00524_0120_A22FLW7LT4/young-po-Micro-C-3ada-12_L6_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/Micro-C-young-pool14_L1_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/young-po-MicroC-rep31_L1_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/Micro-C-young-pool15_L4_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-Micro*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240829_LH00524_0125_A22FLV3LT4/young-po-MicroC-rep32/young-po-MicroC-rep32_L1_G026.R1.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/young_merge.R1.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240716_microrun_microc/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240824_LH00524_0120_A22FLW7LT4/young-po-Micro-C-3ada-12_L6_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/Micro-C-young-pool14_L1_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/young-po-MicroC-rep31_L1_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/Micro-C-young-pool15_L4_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-Micro*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240829_LH00524_0125_A22FLV3LT4/young-po-MicroC-rep32/young-po-MicroC-rep32_L1_G026.R2.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/young_merge.R2.fastq.gz
 
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./young_loop -t 100 -1 ./data/young_merge.R1.fastq.gz -2 ./data/young_merge.R2.fastq.gz -p ./young_loop/young_merge --methods loop
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./old_loop -t 100 -1 ./data/old_merge.R1.fastq.gz -2 ./data/old_merge.R2.fastq.gz -p ./old_loop/old_merge --methods loop
```

**24-10-10** valid pair和细胞数目
```shell
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_R1_001.fastq.gz > scMicro5-GM-Tn5-bead_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_R2_001.fastq.gz > scMicro5-GM-Tn5-bead_R2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_I1_001.fastq.gz > scMicro5-GM-Tn5-bead_I1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_I2_001.fastq.gz > scMicro5-GM-Tn5-bead_I2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_R1_001.fastq.gz > scMicro5-GM_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_R2_001.fastq.gz > scMicro5-GM_R2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_I1_001.fastq.gz > scMicro5-GM_I1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_I2_001.fastq.gz > scMicro5-GM_I2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scMicro5-GM_R1_001.fastq.gz -f2 scMicro5-GM_R2_001.fastq.gz -o ../clean_data/scMicro5-GM -i CTGTCTCTTATACACATCTCCGAG
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scMicro5-GM-Tn5-bead_R1_001.fastq.gz -f2 scMicro5-GM-Tn5-bead_R2_001.fastq.gz -o ../clean_data/scMicro5-GM-Tn5-bead -i CTGTCTCTTATACACATCTCCGAG

seqkit stat *R1_001.fastq.gz
seqkit stat *_trim_index_1.fq

## valid pair
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./qc -t 100 -1 ./clean_data/scMicro5-GM-Tn5-bead_trim_index_1.fq -2 ./clean_data/scMicro5-GM-Tn5-bead_trim_index_2.fq -p ./qc/scMicro5-GM-Tn5-bead --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./qc -t 100 -1 ./clean_data/scMicro5-GM_trim_index_1.fq -2 ./clean_data/scMicro5-GM_trim_index_2.fq -p ./qc/scMicro5-GM --methods MicroC

## 细胞数
mv scMicro5-GM-Tn5-bead_R1_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_R1_001.fastq.gz
mv scMicro5-GM-Tn5-bead_I1_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_I1_001.fastq.gz
mv scMicro5-GM-Tn5-bead_R2_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_R3_001.fastq.gz
mv scMicro5-GM-Tn5-bead_I2_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_R2_001.fastq.gz
mv scMicro5-GM_R1_001.fastq.gz scMicro5-GM_S1_L001_R1_001.fastq.gz
mv scMicro5-GM_I1_001.fastq.gz scMicro5-GM_S1_L001_I1_001.fastq.gz
mv scMicro5-GM_R2_001.fastq.gz scMicro5-GM_S1_L001_R3_001.fastq.gz
mv scMicro5-GM_I2_001.fastq.gz scMicro5-GM_S1_L001_R2_001.fastq.gz
bash 1.sh scMicro5-GM 1>scMicro5-GM.txt 2>&1
bash 2.sh scMicro5-GM-Tn5-bead 1>scMicro5-GM-Tn5-bead.txt 2>&1
```