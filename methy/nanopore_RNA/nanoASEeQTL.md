```Shell
python /mnt/hpc/home/xuxinran/DirectSeq/nanoASEqtl/1_get_eqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt

# 实际运行
base run1.sh

## 2、fisher检验
/mnt/hpc/home/xuxinran/DirectSeq/nanoASEqtl/2_fdr.ipynb

rm *_haplotype_chr*_tmp.csv
```

