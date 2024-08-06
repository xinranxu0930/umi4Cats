rmdupPath="/mnt/hpc/home/xuxinran/microC/loopqtl_data/duplicated.py"
plotR="/mnt/hpc/home/xuxinran/microC/loopqtl_data/plot_fun.R"
ref="/mnt/hpc/home/xuxinran/microC/loopqtl_data/genome.fa"
location="/mnt/hpc/home/xuxinran/microC/loopqtl_data/HUVEC_imputed.locations.bed.gz"
genotype="/mnt/hpc/home/xuxinran/microC/loopqtl_data/HUVEC_imputed.genotypes.txt.gz"
individual="/mnt/hpc/home/xuxinran/microC/loopqtl_data/HUVEC_imputed.individuals.txt.gz"
depth=20

FILE="yo_pooling_microC_sorted.bam"
prefix="yo_pooling_microC"

#比对
bowtie2 -p 100 -x /mnt/hpc/home/xuxinran/REF/hg19/Sequence/Bowtie2Index/hg19 -1 /mnt/hpc/home/xuxinran/microC/date/date_0408_oldmccloop_mccpaittools_micrors/data/mcc_old/MCC-old-po_R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/date/date_0408_oldmccloop_mccpaittools_micrors/data/mcc_old/MCC-old-po_R2.fastq.gz | samtools view -S -b -q 10 - > MCC-old-po.bam

sambamba sort -t 50 -o MCC-old-po_bowtie2-sorted.bam MCC-old-po_bowtie2.bam

python /mnt/hpc/home/xuxinran/microC/cisVar/cisVar.py mpileup -F $prefix -f $ref -B $FILE -p $location -r $depth
python /mnt/hpc/home/xuxinran/microC/cisVar/cisVar1.py post -F $prefix -a $genotype -r $depth

mv ${prefix}.${depth}.POSTth.txt ${prefix}.${depth}.POSTth.dup.txt
python $rmdupPath ${prefix} $depth

python /mnt/hpc/home/xuxinran/microC/cisVar/cisVar1.py geno -F $prefix -i $individual -g $genotype -r $depth
python /mnt/hpc/home/xuxinran/microC/cisVar/cisVar1.py qtls -F $prefix -r $depth

