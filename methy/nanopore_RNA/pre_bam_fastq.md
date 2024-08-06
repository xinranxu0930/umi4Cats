# 前期须知
**1、绘图颜色**

![绘图颜色](./2024-07-08.png)

<span style="background-color:#845EC2; color:white;">#845EC2</span> 
<span style="background-color:#2C73D2; color:white;">#2C73D2</span> 
<span style="background-color:#0081CF; color:white;">#0081CF</span> 
<span style="background-color:#0089BA; color:white;">#0089BA</span> 
<span style="background-color:#008E9B; color:white;">#008E9B</span> 
<span style="background-color:#008F7A; color:white;">#008F7A</span>

**2、SNP文件**

提前准备snp的txt文件，header可以不一样，但是顺序要一样
- 有genotype，plink后将frq文件整理为标准格式

```shell
plink --bfile /mnt/hpc/home/xuxinran/huvec_genotype/huvec_imputed --freq --out /mnt/hpc/home/xuxinran/huvec_genotype/allele_frequencies
```
- 没有genotype，用对应的SNP vcf注释文件整理为标准格式
|CHR|pos|SNP|A1|A2|MAF|

| CHR | pos | SNP | A1 | A2 | MAF |
| :-: | :-: | :-: | :-: | :-: | :-: |
| chr1 | 16002228 | rs72704715 | C | G | 0.01923 |

<span style="color:red;">MAF是A1的频率！</span>

# 所有前期处理
## fast5 2 pod5
```shell
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5

pod5 convert fast5 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/20240202-zhaolin-RNA-2/old/fast5_pass/*.fast5 --strict --output old_2_pass.pod5
```

## basecall
```shell
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/mod_basecall

## old1
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > old_1_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > old_1_calls_m6A.bam

## old2
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > old_2_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > old_2_calls_m6A.bam

## yo1
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > yo_1_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > yo_1_calls_m6A.bam

## yo2
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > yo_2_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.0.0_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --secondary no -Y -k 14 > yo_2_calls_m6A.bam
```
## 两种bam 2 fastq 再minimap 添加mod tag
```shell
## bam2fastq

cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A
samtools fastq -T "MM,ML" -@ 100 -0 old_1_calls_m6A.fastq ../../mod_basecall/old_1_calls_m6A.bam
samtools fastq -T "MM,ML" -@ 100 -0 old_2_calls_m6A.fastq ../../mod_basecall/old_2_calls_m6A.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_1_calls_m6A.fastq ../../mod_basecall/yo_1_calls_m6A.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_2_calls_m6A.fastq ../../mod_basecall/yo_2_calls_m6A.bam
cat *_calls_m6A.fastq > nano_merge_calls_m6A.fastq

http://fantom.gsc.riken.jp/5/datafiles/latest/extra/CAGE_peaks/hg19.cage_peak_phase1and2combined_ann.txt.gz

/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.7.2-linux-x64/bin/dorado correct -x cuda:all -m /mnt/hpc/home/xuxinran/DirectSeq/dorado_correct_model/herro-v1 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/nano_merge_calls_m6A.fastq > /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/corrected_reads.fasta

cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/pseU
samtools fastq -T "MM,ML" -@ 100 -0 old_1_calls_pseU.fastq ../../mod_basecall/old_1_calls_pseU.bam
samtools fastq -T "MM,ML" -@ 100 -0 old_2_calls_pseU.fastq ../../mod_basecall/old_2_calls_pseU.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_1_calls_pseU.fastq ../../mod_basecall/yo_1_calls_pseU.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_2_calls_pseU.fastq ../../mod_basecall/yo_2_calls_pseU.bam
cat *_calls_pseU.fastq > nano_merge_calls_pseU.fastq


## minimap2
minimap2 -ax splice -uf -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min nano_merge_calls_pseU.fastq | samtools sort -@ 100 -O BAM -o ../../bam/nano_merge_calls_pseU_sorted.bam
samtools index -@ 20 ../../bam/nano_merge_calls_pseU_sorted.bam

minimap2 -ax splice -uf -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min nano_merge_calls_m6A.fastq | samtools sort -@ 100 -O BAM -o ../../bam/nano_merge_calls_m6A_sorted.bam
samtools index -@ 20 ../../bam/nano_merge_calls_m6A_sorted.bam

## 添加mod tag
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/00_add_modification_tag.py -f /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/nano_merge_calls_m6A.fastq -b nano_merge_calls_m6A_sorted.bam -t 20
samtools index -@ 20 nano_merge_calls_m6A_sorted_mod.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanopseUqtl/00_add_modification_tag.py -f /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/pseU/nano_merge_calls_pseU.fastq -b nano_merge_calls_pseU_sorted.bam -t 20
samtools index -@ 20 nano_merge_calls_pseU_sorted_mod_map.bam

rm nano_merge_calls_pseU_sorted.bam* nano_merge_calls_m6A_sorted.bam*
```

