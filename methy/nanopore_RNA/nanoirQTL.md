# isoform

```Shell
## 比对
flair align -t 100 -g /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19.fa -r /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/nano_merge_calls_m6A.fastq --nvrna -o ./nano_merge

## 矫正
# 该模块使用基因组注释和/或短读剪接连接纠正错位的剪接位点。
flair correct --threads 100 --nvrna -g /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19.fa -o ./nano_merge -q nano_merge.bed -f /mnt/hpc/home/xuxinran/REF/hg19/gencode.v46lift37.annotation.gtf

## 定义转录本
# 不使用注释文件来合并转录本，而是根据共享相同剪接位点链的读取数据定义转录本
# bed文件不能大于1G，超过的话可以根据chr拆分一下
# 拆分bed文件
awk '{if($1 ~ /^chr2/) print > "nano_merge_all_corrected_chr2.bed"; else if($1 ~ /^chr1/) print > "nano_merge_all_corrected_chr1.bed"; else print > "nano_merge_all_corrected_other.bed"}' nano_merge_all_corrected.bed

mkdir ./chr1 ./chr2 ./other
flair collapse --threads 50 -g /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19.fa -q nano_merge_all_corrected_chr1.bed -r /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/nano_merge_calls_m6A.fastq --gtf /mnt/hpc/home/xuxinran/REF/hg19/gencode.v46lift37.annotation.gtf --generate_map --stringent --check_splice --annotation_reliant generate --output ./chr1/nano_merge1 --support 1

flair collapse --threads 50 -g /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19.fa -q nano_merge_all_corrected_chr2.bed -r /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/nano_merge_calls_m6A.fastq --gtf /mnt/hpc/home/xuxinran/REF/hg19/gencode.v46lift37.annotation.gtf --generate_map --stringent --check_splice --annotation_reliant generate --output ./chr2/nano_merge2 --support 1

flair collapse --threads 50 -g /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19.fa -q nano_merge_all_corrected_other.bed -r /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/fastq/m6A/nano_merge_calls_m6A.fastq --gtf /mnt/hpc/home/xuxinran/REF/hg19/gencode.v46lift37.annotation.gtf --generate_map --stringent --check_splice --annotation_reliant generate --output ./other/nano_merge3 --support 1

cat ./chr1/nano_merge1.combined.isoform.read.map.txt ./chr2/nano_merge2.combined.isoform.read.map.txt ./other/nano_merge3.combined.isoform.read.map.txt > nano_merge.combined.isoform.read.map.txt
```


# qtl

```Shell
## 1、pre.combined.isoform.read.map.txt可能有多个 这里合并 将这些变成一个pkl
python /mnt/hpc/home/xuxinran/DirectSeq/nanoirqtl/1_flair2dict.py -f nano_merge.combined.isoform.read.map.txt -p ./nano_merge
## 2、获取snp和snp所在read的isoform分类之间数量表格（多分类表
python /mnt/hpc/home/xuxinran/DirectSeq/nanoirqtl/2_get_irqtl.py -c chr12 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -r nano_merge_isoform_read.pkl -s + --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes

# 实际运行
base run2.sh

## 3、fisher检验


rm *_haplotype_chr*_tmp.csv
```


