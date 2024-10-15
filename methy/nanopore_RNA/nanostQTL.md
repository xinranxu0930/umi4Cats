[提取基因组中的内含子、外显子以及基因间区_bedtools 内含子_Man_in_black_F的博客-CSDN博客](https://blog.csdn.net/weixin_53737233/article/details/127440952)



```R
# 不考虑N，获取bam文件整体的bed文件
bedtools bamtobed -i /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_calls_m6A_sorted_mod_map.bam > nano_merge_calls_sort_map_bam2bed_fullread.bed

## 1、利用gtf获取每个gene的exon和intron位置，获取read和gene的比对情况（没比对到gene的、比对到no intron上的、有效read）
python /mnt/hpc/home/xuxinran/DirectSeq/nanostqtl/1_splitGFT.py

## 2、获取比对到含有intron的gene上的read的bam文件
samtools view -N valid_readID.txt /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_calls_m6A_sorted_mod_map.bam -b > nano_merge_calls_m6A_sorted_mod_map_valid.bam
samtools index -@ 15 nano_merge_calls_m6A_sorted_mod_map_valid.bam
python /mnt/hpc/home/xuxinran/DirectSeq/nanostqtl/0_bam_flag_filter.py -b  nano_merge_calls_m6A_sorted_mod_map_valid.bam -p ./nano_merge -t 20 -m strand
samtools index -@ 15 nano_merge_map0.bam
samtools index -@ 15 nano_merge_map16.bam
bedtools bamtobed -splitD -i nano_merge_calls_m6A_sorted_mod_map_valid.bam > nano_merge_calls_sort_map_valid_bam2bed.bed # 后面要算长度，所以这里考虑N和D再将bam转成bed

## 2、计算每个read对应的exon和intron数量，计算read的RNA稳定性
sort -k 1,1 -k2,2n nano_merge_calls_sort_map_valid_bam2bed.bed > nano_merge_calls_sort_map_valid_bam2bed_sort.bed

bedtools intersect -s -a nano_merge_calls_sort_map_valid_bam2bed_sort.bed -b intron.bed > nano_merge_intron.bed

bedtools intersect -s -a nano_merge_calls_sort_map_valid_bam2bed_sort.bed -b exon_merge.bed  > nano_merge_exon.bed

python /mnt/hpc/home/xuxinran/DirectSeq/nanostqtl/2_read_stability.py
## 3、计算qtl
python /mnt/hpc/home/xuxinran/DirectSeq/nanostqtl/3_get_stqtl.py -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/min_qscore_0/mod_bam/merge/nano_merge_calls_sort_map0.bam -p ./nano_merge --readST nano_merge_read_stability.csv -c chr1 -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 
# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/nanostqtl/run3.sh


rm nano_merge_haplotype* nano_merge_map* nano_merge_intron.bed nano_merge_exon.bed nano_merge_calls_sort_map_valid_bam2bed_sort.bed nano_merge_calls_sort_map_valid_bam2bed.bed
```

