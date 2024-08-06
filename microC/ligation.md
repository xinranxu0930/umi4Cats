首先得到qc文件，这里可以得到total trans >1kb dup的数量

pair_type_count.ipynb 统计 both-M single-M both-N single-N

```Shell
pairsam_file="../Micro-C-K562_S17_L001_dedup.pairsam"
output_csv="Micro-C_valid_id.txt"
# 提取undep map read id
awk 'BEGIN {FS="\t"; OFS="\t"} !/^#/ && ($8 == "RU" || $8 == "UR" || $8 == "uU" || $8 == "uu" || $8 == "Uu" || $8 == "UU") {print $1, $2, $3, $4, $5, $6, $7}' $pairsam_file > $output_csv
cut -f1 $output_csv > Micro-C_only_valid_id.txt
samtools view -@ 100 -bS ../MCUT-A_S13_L001_aligned.sam > MCUT-A_S13_L001_aligned.bam
sambamba sort -t 100 MCUT-A_S13_L001_aligned.bam -o MCUT-A_S13_L001_aligned_sort.bam
# 01.ipynb 拆分only_valid_id.txt
# bash 01.sh # 根据子only_valid_id.txt拆分sam文件
# 数据小就直接跳过 01.sh
samtools view -@ 100 -b -h -N MCUT-A_only_valid_id.txt MCUT-A_S13_L001_aligned_sort.bam > MCUT-A_S13_L001_aligned_ligation_tmp.bam
# bash 015.sh # 对新的bam子文件排序
sambamba sort -t 100 MCUT-A_S13_L001_aligned_ligation_tmp.bam -o MCUT-A_S13_L001_aligned_ligation_sort_tmp.bam

python /mnt/hpc/home/xuxinran/microC/unligation/02.py
rm *_tmp*

# test.ipynb 统计unliagtion,<1kb	

```



# 统计三种read seq len

```Shell
awk -F'\t' '$2 == $4' K562-MCUT_valid_id.txt > K562-MCUT_cis_map.txt
/mnt/hpc/home/xuxinran/microC/unligation/test.ipynb

seqkit grep -f K562-MCUT_less1k.txt /mnt/hpc/home/xuxinran/microC/date/date_0522/trim_data/K562-MCUT_trim_1.fq -o K562-MCUT_less1k_1.fq
seqkit grep -f K562-MCUT_less1k.txt /mnt/hpc/home/xuxinran/microC/date/date_0522/trim_data/K562-MCUT_trim_2.fq -o K562-MCUT_less1k_2.fq
seqkit grep -f K562-MCUT_more1k.txt /mnt/hpc/home/xuxinran/microC/date/date_0522/trim_data/K562-MCUT_trim_1.fq -o K562-MCUT_more1k_1.fq
seqkit grep -f K562-MCUT_more1k.txt /mnt/hpc/home/xuxinran/microC/date/date_0522/trim_data/K562-MCUT_trim_2.fq -o K562-MCUT_more1k_2.fq
seqkit grep -f K562-MCUT_unligation.txt /mnt/hpc/home/xuxinran/microC/date/date_0522/trim_data/K562-MCUT_trim_1.fq -o K562-MCUT_unligation_1.fq
seqkit grep -f K562-MCUT_unligation.txt /mnt/hpc/home/xuxinran/microC/date/date_0522/trim_data/K562-MCUT_trim_2.fq -o K562-MCUT_unligation_2.fq

mkdir more1k less1k unligation
flash -t 15 K562-MCUT_more1k_1.fq K562-MCUT_more1k_2.fq --output-prefix=K562-MCUT_more1k-flash --output-directory=./more1k
flash -t 15 K562-MCUT_less1k_1.fq K562-MCUT_less1k_2.fq --output-prefix=K562-MCUT_less1k-flash --output-directory=./less1k
flash -t 15 K562-MCUT_unligation_1.fq K562-MCUT_unligation_2.fq --output-prefix=K562-MCUT_unligation-flash --output-directory=./unligation

```







