bwa mem -5SP -T0 -t100 /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa old-po-microc-52_L4_Q0063W0181.R1.fastq.gz old-po-microc-52_L4_Q0063W0181.R2.fastq.gz -o old-po-microc-52_L4_aligned.sam
pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 100 --nproc-out 100 --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes old-po-microc-52_L4_aligned.sam > old-po-microc-52_L4_parsed.pairsam
pairtools sort --tmpdir ./tmp --nproc 100 old-po-microc-52_L4_parsed.pairsam > old-po-microc-52_L4_sorted.pairsam
pairtools dedup --nproc-in 100 --nproc-out 100 --mark-dups --max-mismatch 3 --backend cython --output-stats old-po-microc-52_L4_stats.txt --output old-po-microc-52_L4_dedup.pairsam old-po-microc-52_L4_sorted.pairsam

pairtools split --nproc-in 50 --nproc-out 50 --output-pairs MCC-old-po_mapped.pairs --output-sam MCC-old-po_unsorted.bam /mnt/hpc/home/xuxinran/microC/date/date_0408_oldmccloop_mccpaittools_micrors/mcc_pairtools/old/MCC-old-po_dedup.pairsam

java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 50 MCC-old-po_mapped.pairs MCC-old-po_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes

java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 50 -r 5000,10000 --ignore-sparsity MCC-old-po_contact_map.hic MCC-old-po_hic.hiccups

