[得到一个物种所有基因的TSS(转录起始位点)区域的bed文件。 | 生信菜鸟团](http://www.bio-info-trainee.com/2494.html)

```Shell
## 制作TSS bed文件
wget https://fantom.gsc.riken.jp/5/datafiles/phase1.3/extra/TSS_classifier/TSS_human.bed.gz
/mnt/hpc/home/xuxinran/DirectSeq/nanotssqtl/1_getTSSbed.ipynb

## 获取read对应的TSS
/mnt/hpc/home/xuxinran/DirectSeq/nanotssqtl/2_read2fantom.ipynb

## call tuqtl
python /mnt/hpc/home/xuxinran/DirectSeq/nanotssqtl/3_get_puqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 -f nano_merge_overlap.bed --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt
# 实际运行/mnt/hpc/home/xuxinran/DirectSeq/nanotssqtl/run3.sh

/mnt/hpc/home/xuxinran/DirectSeq/nanotssqtl/4_fdr.ipynb
rm nano_merge_haplotype_*
```



