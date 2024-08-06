#将read map到ref_gen后生成SAM文件
bwa mem -5SP -T0 -t8 ~/REF/hg19/BWAIndex/genome /f/xinran/MicroC/xueqi_data/00.CleanData/3-Huvec-T4/3-Huvec-T4_1.clean.fq.gz /f/xinran/MicroC/xueqi_data/00.CleanData/3-Huvec-T4/3-Huvec-T4_2.clean.fq.gz -o 3_Huvec_T4_aligned.sam

bwa mem -5SP -T0 -t8 ~/REF/hg19/BWAIndex/genome /f/xinran/MicroC/xueqi_data/00.CleanData/4-Huvec-Ex/4-Huvec-Ex_1.clean.fq.gz /f/xinran/MicroC/xueqi_data/00.CleanData/4-Huvec-Ex/4-Huvec-Ex_2.clean.fq.gz -o 4_Huvec_Ex_aligned.sam

#在aligned.sam中识别ligation
pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 8 --nproc-out 8 --chroms-path /f/xinran/REF/hg19/hg19.chrom.sizes 3_Huvec_T4_aligned.sam >  3_Huvec_T4_parsed.pairsam

pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 8 --nproc-out 8 --chroms-path /f/xinran/REF/hg19/hg19.chrom.sizes 4_Huvec_Ex_aligned.sam >  4_Huvec_Ex_parsed.pairsam

#排序
pairtools sort --nproc 16 4_Huvec_Ex_parsed.pairsam > 4_Huvec_Ex_sorted.pairsam

pairtools sort --nproc 16 3_Huvec_T4_parsed.pairsam > 3_Huvec_T4_sorted.pairsam

#去除PCR重复
pairtools dedup --nproc-in 8 --nproc-out 8 --mark-dups --output-stats 4_Huvec_Ex_stats.txt --output 4_Huvec_Ex_dedup.pairsam 4_Huvec_Ex_sorted.pairsam

pairtools dedup --nproc-in 8 --nproc-out 8 --mark-dups --output-stats 3_Huvec_T4_stats.txt --output 3_Huvec_T4_dedup.pairsam 3_Huvec_T4_sorted.pairsam

#将.pairsam分为sam文件+pairs文件
pairtools split --nproc-in 8 --nproc-out 8 --output-pairs 3_Huvec_T4_mapped.pairs --output-sam 3_Huvec_T4_unsorted.bam 3_Huvec_T4_dedup.pairsam

pairtools split --nproc-in 8 --nproc-out 8 --output-pairs 4_Huvec_Ex_mapped.pairs --output-sam 4_Huvec_Ex_unsorted.bam 4_Huvec_Ex_dedup.pairsam

#排序，mapped.PT.bam是将在下游步骤中使用的最终bam文件
samtools sort -@16 -o 3_Huvec_T4_mapped.PT.bam 3_Huvec_T4_unsorted.bam

samtools sort -@16 -o 4_Huvec_Ex_mapped.PT.bam 4_Huvec_Ex_unsorted.bam

#索引
samtools index 3_Huvec_T4_mapped.PT.bam

samtools index 4_Huvec_Ex_mapped.PT.bam

#QC
python3 ../../Micro-C-main/get_qc.py -p 3_Huvec_T4_stats.txt > 3_Huvec_T4_qc.txt

python3 ../../Micro-C-main/get_qc.py -p 4_Huvec_Ex_stats.txt > 4_Huvec_Ex_qc.txt

#计算复杂度
preseq lc_extrap -bam -pe -extrap 2.1e9 -step 1e8 -seg_len 1000000000 -output 3_Huvec_T4_out.preseq 3_Huvec_T4_mapped.PT.bam

preseq lc_extrap -bam -pe -extrap 2.1e9 -step 1e8 -seg_len 1000000000 -output 4_Huvec_Ex_out.preseq 4_Huvec_Ex_mapped.PT.bam

#生成互作矩阵
java -Djava.awt.headless=true -jar ../../Micro-C-main/juicertools.jar pre --threads 8 3_Huvec_T4_mapped.pairs 3_Huvec_T4_contact_map.hic /f/xinran/REF/hg19/hg19.chrom.sizes

java -Djava.awt.headless=true -jar ../../Micro-C-main/juicertools.jar pre --threads 8 4_Huvec_Ex_mapped.pairs 4_Huvec_Ex_contact_map.hic /f/xinran/REF/hg19/hg19.chrom.sizes

#提取显著loop
java -Djava.awt.headless=true -jar ../../Micro-C-main/juicertools.jar hiccups --cpu --threads 16 -r 5000,10000 --ignore-sparsity 3_Huvec_T4_contact_map.hic 3_Huvec_T4.hic.hiccups

java -Djava.awt.headless=true -jar ../../Micro-C-main/juicertools.jar hiccups --cpu --threads 16 -r 5000,10000 --ignore-sparsity 4_Huvec_Ex_contact_map.hic 4_Huvec_Ex.hic.hiccups