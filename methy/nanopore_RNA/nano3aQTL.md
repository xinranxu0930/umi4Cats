# 最终方法
```shell
/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/1_read2apadb.ipynb

python /mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/4_get_3aqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 -f nano_merge_overlap.bed --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt

 # 实际运行
 /mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/run2.sh
 ```

 # 旧方法：自己识别
[参考链接](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02502-z)

1、找到cigar中的S，正链是3' 负链是5'，检查长度

  - S<20bp,要求A/T大于总长度的80%

  - S≥20bp

    - 前20bp A≥70%，后20bp A≥80%（正链）

    - 前20bp T≥80%，后20bp T≥70%（负链）

2、找到切割点，取切割点+-10bp的区间，要求这+-10bp中A≤5

3、导出一个PAS区间`[PAS-40 , PAS]`，用于后续查看motif情况；导出PAS位点的情况`[PAS-1 , PAS]`

4、PAS位点和apadb比较 首先看overlap% ；然后查看PAS区间的motif情况

5、PAS位点和apadb的区间合并，挑选出没有被合并的点，将这些点合并为100bp富含PAS位点的区间，并且延伸上游10bp，最终得到110bp的区间，利用geneID给每个PAS命名

6、合并两个结果区间，生成一个新的apa参考数据

7、和read比较 得到read-apa的pkl

```shell
# 所有的gene转bed
/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/00_get_gene_bed.ipynb

# 获取每个read的实际PAS情况
python /mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/1_find_PASsite.py -c chr1 -p ./nano_merge -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa -t 20 -s +
# 实际运行run1.sh

# 验证结果，挑选出不在apadb且含有motif的结果，和apadb合并，获取最终的PAS结果
/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/2_PASres.ipynb
# nano_merge_pas_sorted.bed 找到的所有PAS位点

## 获取正read的3‘端的M段 和 负read的5’端的M段，分别和PAS区间比对，得到read和PAS的pkl文件
# 处理bam文件
bedtools bamtobed -splitD -i /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_calls_m6A_sorted_mod_map.bam > nano_merge_calls_sort_map_bam2bed.bed
awk '$6 == "+" {print > "positive_strand.bed"} $6 == "-" {print > "negative_strand.bed"}' nano_merge_calls_sort_map_bam2bed.bed
# 负链保留第一个；正链反向排序之后保留第一个
awk '!seen[$4]++' negative_strand.bed > negative_strand_res.bed
tac positive_strand.bed | awk '!seen[$4]++' | tac > positive_strand_res.bed
cat negative_strand_res.bed positive_strand_res.bed > nano_merge_read_compare.bed
sort -k 1,1 -k2,2n nano_merge_read_compare.bed > nano_merge_read_compare_sorted.bed
# 获取read和apa的对应关系
bedtools intersect -a nano_merge_read_compare_sorted.bed -b nano_merge_apaREF_sorted_seq.bed -wa -wb -s > nano_merge_polyA_read.bed

/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/3_get_readPAS.ipynb

rm gene_merge.bed *_apaREF_sorted_seq.bed *_calls_sort_map_bam2bed.bed *_polyA_read.bed *_read_compare.bed *_read_compare_sorted.bed negative_strand_res.bed positive_strand_res.bed positive_strand.bed negative_strand.bed

## call apaqtl
python /mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/4_get_3aqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 --pkl /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/apa/read2apa.pkl
# 实际运行
base run4.sh

## fisher检验
/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/5_fdr.ipynb

rm *_haplotype_chr*_tmp.csv
```