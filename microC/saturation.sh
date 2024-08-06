mkdir /f/xinran/MicroC/saturation/MicroC/2-230815-230901_old-po-Micro-C-rep5
cd /f/xinran/MicroC/saturation/MicroC/2-230815-230901_old-po-Micro-C-rep5

cat /f/xinran/MicroC/microC_xueqi/xueqi_230815/20230812_AHHMCYDSX7_U1275_TJYKDXWXQ-20230812/RawData/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S91_L002_R1_001.fastq.gz /f/xinran/MicroC/microC_xueqi/xueqi_230901/20230820_AH2FCYDSX7_U1275_TJYKDXWXQ-20230820/RawData/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S29_L001_R1_001.fastq.gz > old-po-Micro-C-rep5_S29_L001_R1_merge.fastq.gz
cat /f/xinran/MicroC/microC_xueqi/xueqi_230815/20230812_AHHMCYDSX7_U1275_TJYKDXWXQ-20230812/RawData/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S91_L002_R2_001.fastq.gz /f/xinran/MicroC/microC_xueqi/xueqi_230901/20230820_AH2FCYDSX7_U1275_TJYKDXWXQ-20230820/RawData/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S29_L001_R2_001.fastq.gz > old-po-Micro-C-rep5_S29_L001_R2_merge.fastq.gz

python /f/xinran/some_code/microc-preseq.py -1 old-po-Micro-C-rep5_S29_L001_R1_merge.fastq.gz -2 old-po-Micro-C-rep5_S29_L001_R2_merge.fastq.gz -o old-po-Micro-C-rep5_S29_L001

rm *.fq.gz