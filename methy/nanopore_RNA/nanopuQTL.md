```Shell
# 合并CAGEpeak为promoter 和read overlap
python python /mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/1_read2promoter.py

# 识别qtl
python /mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/2_get_puqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 -f nano_merge_overlap_uniq.bed --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt
#实际运行 /mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/run2.sh

/mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/3_fdr.ipynb
rm nano_merge_haplotype_*



sort -k1,1 -k2,2n cage.bed -o cage_sorted.bed
bedtools merge -i cage_sorted.bed -d 200 -s -c 4,5,6 -o collapse > promoter_merge.bed

```



