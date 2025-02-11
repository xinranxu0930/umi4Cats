## dongqing_1014
viewpoint:TATATAGAAAACAAGACAGACAC PTPN1 chr20:49100767-49100789
酶：NlaIII CATG↓
感兴趣的区域：chr20:49124920-49127000(49126920)
AAGGAGGCATTAAACAGCTAAATACA CATG

```shell
python /mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py -f1 /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/data/S1824
# S1824: {'total': 27649009, 'valid reads number': 857383, 'valid reads ratio': '0.03', 'unvalid reads number': 26791626, 'unvalid reads ratio': '0.97'}

python /mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py -f1 /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/data/z12gctr
# z12gctr: {'total': 71070782, 'valid reads number': 977346, 'valid reads ratio': '0.01', 'unvalid reads number': 70093436, 'unvalid reads ratio': '0.99'}

seqkit stat * # 109

python /mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py -f1 S1824_1_PTPN1_tmp_R1.fq -f2 S1824_1_PTPN1_tmp_R2.fq -m 109
python /mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py -f1 z12gctr_1_PTPN1_tmp_R1.fq -f2 z12gctr_1_PTPN1_tmp_R2.fq -m 109

seqkit stat * # 检查
rm *tmp*
```

```R
library(UMI4Cats)
hg19_NlaIII <- digestGenome(
    cut_pos = 4,
    res_enz = "CATG",
    name_RE = "NlaIII",
    ref_gen = BSgenome.Hsapiens.UCSC.hg19::BSgenome.Hsapiens.UCSC.hg19,
    out_path = file.path("/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014", "digested_genome/")
)
contactsUMI4C(
    fastq_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/data",
    wk_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/workdir",
    bait_seq = "AAACAGCTAAATACA",
    bait_pad = "",
    res_enz = "CATG",
    cut_pos = 4,
    digested_genome = '/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/digested_genome/BSgenome.Hsapiens.UCSC.hg19_NlaIII',
    bowtie_index = "/mnt/hpc/home/xuxinran/REF/hg19/Sequence/Bowtie2Index/hg19",
    ref_gen = BSgenome.Hsapiens.UCSC.hg19::BSgenome.Hsapiens.UCSC.hg19,
    threads = 10
)
library(ggplot2)
plot <- statsUMI4C(wk_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/workdir")
ggsave(filename = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/workdir/statsUMI4C_plot.png", plot = plot, width = 8, height = 6)

files <- list.files(file.path("/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/workdir", "count"), pattern = "*_counts.tsv.gz", full.names = TRUE) ## 获取所有的tsv文件
colData <- data.frame(
    sampleID = gsub("_counts.tsv.gz", "", basename(files)),
    file = files,
    stringsAsFactors = FALSE
)

library(tidyr)
colData <- colData %>%
    separate(sampleID, into = c("condition", "replicate", "viewpoint"), remove = FALSE)
umi <- makeUMI4C(
    colData = colData,
    viewpoint_name = "viewpoint",
    grouping = "condition"
)
colors <- c("S1824" = "purple", "z12gctr" = "orange")
pdf('/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/workdir/makeUMI4C.pdf',height = 8,width = 12)
plot.new()
plotUMI4C(umi,
    grouping = "condition",
    dgram_plot = FALSE,
    ylim = c(0, 4),
    xlim = c(49100000,49126956),
    colors = colors
)
legend("topright", legend = names(colors), fill = colors, title = "Conditions")
dev.off()

```



## dongqing_1101
```shell
cd /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/data
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/S1824_L4_Q0799.R1.fastq.gz > S1824_raw.R1.fastq.gz

cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/S1824_L4_Q0799.R2.fastq.gz > S1824_raw.R2.fastq.gz

cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/z12g-ctr_L4_G028.R1.fastq.gz > z12gctr_raw.R1.fastq.gz

cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/z12g-ctr_L4_G028.R2.fastq.gz > z12gctr_raw.R2.fastq.gz


python /mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py -f1 S1824_raw.R1.fastq.gz -f2 S1824_raw.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./S1824
# {'sample': 'S1824', 'total': 45946062, 'valid reads number': 858809, 'valid reads ratio': '0.02', 'unvalid reads number': 45087253, 'unvalid reads ratio': '0.98'}

python /mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py -f1 z12gctr_raw.R1.fastq.gz -f2 z12gctr_raw.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./z12gctr
# {'sample': 'z12gctr', 'total': 94877165, 'valid reads number': 979228, 'valid reads ratio': '0.01', 'unvalid reads number': 93897937, 'unvalid reads ratio': '0.99'}

seqkit stat * # 109

python /mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py -f1 S1824_1_PTPN1_tmp_R1.fq -f2 S1824_1_PTPN1_tmp_R2.fq -m 88
python /mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py -f1 z12gctr_1_PTPN1_tmp_R1.fq -f2 z12gctr_1_PTPN1_tmp_R2.fq -m 88

seqkit stat * # 检查
rm *tmp*
```

```R
library(UMI4Cats)

contactsUMI4C(
    fastq_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/data/clean",
    wk_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/workdir",
    bait_seq = "AAACAGCTAAATACA",
    bait_pad = "",
    res_enz = "CATG",
    cut_pos = 4,
    digested_genome = '/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1014/digested_genome/BSgenome.Hsapiens.UCSC.hg19_NlaIII',
    bowtie_index = "/mnt/hpc/home/xuxinran/REF/hg19/Sequence/Bowtie2Index/hg19",
    ref_gen = BSgenome.Hsapiens.UCSC.hg19::BSgenome.Hsapiens.UCSC.hg19,
    threads = 10
)
library(ggplot2)
plot <- statsUMI4C(wk_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/workdir")
ggsave(filename = "/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/workdir/statsUMI4C_plot.png", plot = plot, width = 8, height = 6)

files <- list.files(file.path("/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/workdir", "count"), pattern = "*_counts.tsv.gz", full.names = TRUE) ## 获取所有的tsv文件
colData <- data.frame(
    sampleID = gsub("_counts.tsv.gz", "", basename(files)),
    file = files,
    stringsAsFactors = FALSE
)

library(tidyr)
colData <- colData %>%
    separate(sampleID, into = c("condition", "replicate", "viewpoint"), remove = FALSE)
umi <- makeUMI4C(
    colData = colData,
    viewpoint_name = "viewpoint",
    grouping = "condition",
    bait_expansion = 2e6
)
win_frags <- makeWindowFragments(umi, n_frags=8)
gr <-  callInteractions(umi4c = umi,
                        design = ~condition,
                        query_regions = win_frags,
                        padj_threshold = 0.2,
                        zscore_threshold=1,
                        alpha = 10,
                        penalty = 0.05 )

inter <- getSignInteractions(gr)
umi_fisher <- fisherUMI4C(umi,
                          grouping = "condition",
                          query_regions = inter,
                          filter_low = 1)


colors <- c("S1824" = "purple", "z12gctr" = "orange")
pdf('/mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/workdir/makeUMI4C.pdf',height = 8,width = 12)
plot.new()
plotUMI4C(umi,
    grouping = "condition",
    dgram_plot = FALSE,
    ylim = c(0, 4),
    xlim = c(49100000,49126920),
    colors = colors
)
legend("topright", legend = names(colors), fill = colors, title = "Conditions")
dev.off()

```



```shell
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/S1824_L4_Q0799.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/qianting_241114/20241107_LH00708_0013_B22JK2NLT4/S1824-UMI4C/S1824-UMI4C_L3_G044.R1.fastq.gz > S1824.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/S1824_L4_Q0799.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/qianting_241114/20241107_LH00708_0013_B22JK2NLT4/S1824-UMI4C/S1824-UMI4C_L3_G044.R2.fastq.gz > S1824.R2.fastq.gz

cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/z12g-ctr_L4_G028.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/qianting_241114/20241107_LH00708_0013_B22JK2NLT4/cas-12g-DOX-UMI4C/cas-12g-DOX-UMI4C_L3_G053.R1.fastq.gz > z12g-ctr.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/z12g-ctr_L4_G028.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/qianting_241114/20241107_LH00708_0013_B22JK2NLT4/cas-12g-DOX-UMI4C/cas-12g-DOX-UMI4C_L3_G053.R2.fastq.gz > z12g-ctr.R2.fastq.gz

python /mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py -f1 S1824.R1.fastq.gz -f2 S1824.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./clean/S1824
# {'sample': './clean/S1824', 'total': 65454682, 'valid reads number': 859138, 'valid reads ratio': '0.01', 'unvalid reads number': 64595544, 'unvalid reads ratio': '0.99'}


python /mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py -f1 z12g-ctr.R1.fastq.gz -f2 z12g-ctr.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./clean/z12gctr
# {'sample': './clean/z12gctr', 'total': 117485052, 'valid reads number': 979336, 'valid reads ratio': '0.01', 'unvalid reads number': 116505716, 'unvalid reads ratio': '0.99'}

seqkit stat * # 109

python /mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py -f1 S1824_1_PTPN1_tmp_R1.fq -f2 S1824_1_PTPN1_tmp_R2.fq -m 88
python /mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py -f1 z12gctr_1_PTPN1_tmp_R1.fq -f2 z12gctr_1_PTPN1_tmp_R2.fq -m 109

seqkit stat * # 检查
rm *tmp*
```

**24-11-17**
```shell
cat /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/data/S1824_raw.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0068W0388.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0679W0388.R1.fastq.gz > S1824_raw.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/data/S1824_raw.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0068W0388.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0679W0388.R2.fastq.gz > S1824_raw.R2.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/data/z12gctr_raw.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12g-ctr/z12g-ctr_L5_G028.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12gctr/z12gctr_L5_Q0680W0388.R1.fastq.gz > z12gctr_raw.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_1101/data/z12gctr_raw.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12g-ctr/z12g-ctr_L5_G028.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12gctr/z12gctr_L5_Q0680W0388.R2.fastq.gz > z12gctr_raw.R2.fastq.gz

python /mnt/hpc/home/xuxinran/4C/get_viewpoint.py -f1 S1824_raw.R1.fastq.gz -f2 S1824_raw.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./S1824
# S1824: {'sample': './S1824', 'total': 105275475, 'valid reads number': 2140563, 'valid reads ratio': '0.02', 'unvalid reads number': 103134912, 'unvalid reads ratio': '0.98'}

python /mnt/hpc/home/xuxinran/4C/get_viewpoint.py -f1 z12gctr_raw.R1.fastq.gz -f2 z12gctr_raw.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./z12gctr
# z12gctr: {'sample': './z12gctr', 'total': 146779710, 'valid reads number': 1447130, 'valid reads ratio': '0.01', 'unvalid reads number': 145332580, 'unvalid reads ratio': '0.99'}

seqkit stat *tmp* # 109

python /mnt/hpc/home/xuxinran/4C/flat_readlen.py -f1 S1824_1_PTPN1_tmp_R1.fq -f2 S1824_1_PTPN1_tmp_R2.fq -m 71
python /mnt/hpc/home/xuxinran/4C/flat_readlen.py -f1 z12gctr_1_PTPN1_tmp_R1.fq -f2 z12gctr_1_PTPN1_tmp_R2.fq -m 70

seqkit stat * # 检查
rm *tmp*

```

**24-11-17**
```shell
cd /mnt/hpc/home/xuxinran/4C/UMI4C/date/dongqing_0113
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/S1824_L4_Q0799.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0068W0388.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0679W0388.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250104_LH00708_0055_A22K7M5LT4/S1824/S1824_L1_G044.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250107_LH00524_0225_A22K7YTLT4/S1824/S1824_L1_G044.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250110_LH00308_0334_B22KGHTLT4/S1824/S1824_L3_G044.R1.fastq.gz > S1824_raw_merge.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/20240925_LH00524_0147_A22H7CCLT4/S1824/S1824_L6_Q0103.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/S1824_L4_Q0799.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0068W0388.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/S1824/S1824_L5_Q0679W0388.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250104_LH00708_0055_A22K7M5LT4/S1824/S1824_L1_G044.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250107_LH00524_0225_A22K7YTLT4/S1824/S1824_L1_G044.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250110_LH00308_0334_B22KGHTLT4/S1824/S1824_L3_G044.R2.fastq.gz > S1824_raw_merge.R2.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/z12g-ctr_L4_G028.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12g-ctr/z12g-ctr_L5_G028.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12gctr/z12gctr_L5_Q0680W0388.R1.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250104_LH00708_0055_A22K7M5LT4/Z12g/Z12g_L1_G053.R1.fastq.gz > Z12g_raw_merge.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241011/ABFC20240368-53-12g/z12gctr_L5_G026.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241101/ABFC20240368-69/20241021_LH00308_0271_B22H75WLT4/z12g-ctr_L4_G028.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12g-ctr/z12g-ctr_L5_G028.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_241127/ABFC20240368-98/20241122_LH00708_0023_A22JJYKLT4/z12gctr/z12gctr_L5_Q0680W0388.R2.fastq.gz /mnt/hpc/home/xuxinran/4C/UMI4C/data/dongqing_250113/ABFC20241429-27/20250104_LH00708_0055_A22K7M5LT4/Z12g/Z12g_L1_G053.R2.fastq.gz > Z12g_raw_merge.R2.fastq.gz

python /mnt/hpc/home/xuxinran/4C/get_viewpoint.py -f1 S1824_raw_merge.R1.fastq.gz -f2 S1824_raw_merge.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./S1824
python /mnt/hpc/home/xuxinran/4C/get_viewpoint.py -f1 Z12g_raw_merge.R1.fastq.gz -f2 Z12g_raw_merge.R2.fastq.gz -v AAACAGCTAAATACA -e CATG -n PTPN1 -o ./Z12g

python /mnt/hpc/home/xuxinran/4C/flat_readlen.py -f1 S1824_1_PTPN1_tmp_R1.fq -f2 S1824_1_PTPN1_tmp_R2.fq -m 81
python /mnt/hpc/home/xuxinran/4C/flat_readlen.py -f1 Z12g_1_PTPN1_tmp_R1.fq -f2 Z12g_1_PTPN1_tmp_R2.fq -m 73
```