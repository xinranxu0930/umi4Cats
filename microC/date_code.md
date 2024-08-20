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