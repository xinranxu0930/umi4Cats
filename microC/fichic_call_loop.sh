mkdir -p data/yo-po-MC
ln -s /f/xinran/MicroC/microC_xueqi/xueqi_231023_mcc/X101SC23023714-Z01-J006/00.CleanData/young-mcc-po-rep2/young-mcc-po-rep2_1.clean.fq.gz data/yo-po-MC/young-mcc-po-rep2_1.clean.fq.gz 
ln -s /f/xinran/MicroC/microC_xueqi/xueqi_231023_mcc/X101SC23023714-Z01-J006/00.CleanData/young-mcc-po-rep2/young-mcc-po-rep2_2.clean.fq.gz data/yo-po-MC/young-mcc-po-rep2_2.clean.fq.gz 
cp /f/xinran/MicroC/HiC-Pro_3.1.0/config-hicpro.txt .
#修改config文件
/f/xinran/MicroC/HiC-Pro_3.1.0/bin/HiC-Pro -i ./data/ -o ./hicpro_output -c config-hicpro.txt


mkdir ./fithic_res/

python /f/xinran/MicroC/HiC-Pro_3.1.0/bin/utils/hicpro2fithic.py -i ./hicpro_output/hic_results/matrix/yo-po-MC/raw/20000/yo-po-MC_20000.matrix -b ./hicpro_output/hic_results/matrix/yo-po-MC/raw/20000/yo-po-MC_20000_abs.bed -s /f/xinran/MicroC/fithic_call_loop/mcc_231023/hicpro_output/hic_results/matrix/yo-po-MC/iced/20000/yo-po-MC_20000_iced.matrix.biases -o ./fithic_res


cd /f/xinran/MicroC/fithic_call_loop/mcc_231023/fithic_res

zcat fithic.biases.gz | awk 'NF>=3'  > filtered.biases
gzip filtered.biases

fithic -f fithic.fragmentMappability.gz -i fithic.interactionCounts.gz -t filtered.biases.gz -o . -l 1-yo-po-mcc-merge -v -x intraOnly -r 20000