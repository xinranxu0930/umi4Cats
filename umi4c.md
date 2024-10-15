## 文章内容

UMI-4C是对4C的改进 他可以看viewpoint和全基因组中哪些位置有互作 为了避免PCR偏差 加入了UMI 将UMI连接到和viewpoint互作的DNA片段中 然后再进行PCR

高深度测序的期望：当对文库进行高深度测序时，研究者预期映射到每个UMI的reads数量会随着分子数量的一致增加而增加。
4C接触的期望：他们还预期，随着覆盖度的增加，4C图谱中的跨染色体（trans-chromosomal）接触比例应该保持恒定。

偏差1：部分UMI只被少量reads覆盖，即使在高深度测序下，部分UMI仍然只被一两个reads覆盖。研究者推测这些可能是在PCR扩增或测序过程中，出现一些错误事件，导致非目标区域的基因组序列意外地与真正的目标序列（即你感兴趣的基因区域或模板）发生连接。
偏差2：在同一个DNA片段中，一些UMI有很深的测序覆盖度，而其他UMI却只有很低的覆盖度。可能是因为某些UMI代表的DNA片段在扩增或测序过程中因合成或测序错误而发生了低效的扩增或检测。

偏差1解决：
- 噪声过滤：通过基于read覆盖度的统计信息来过滤潜在的伪影，可以消除由上述两种情况引入的噪声。这种过滤确保随着测序深度的增加，所检测到的分子数量可以收敛（即不再随着测序深度的增加而不断增加）。
- 避免假阳性跨染色体接触：防止覆盖多个UMI的反式染色体接触比例持续增加
偏差2解决：
- 基于统计模型来设定一个阈值，过滤掉那些只被一两个reads覆盖的UMI

在较低的测序深度下（如50,000个reads）能检测到大约60%的UMI，而在更高的测序深度（如500,000个reads）能检测到超过90%的UMI

检测多个viewpoint的相互作用
UMI-4C通过引入多个forward引物（每个引物对应不同的viewpoint），可以实现一次实验中检测多个viewpoint的全基因组互作情况。
forward引物用于区分不同的viewpoint，而reverse引物负责扩增。这意味着，在实验过程中，多个viewpoint可以通过不同的forward引物同时检测。后续根据这些不同的forward引物，生成多个FASTQ文件，用来分析不同viewpoint的基因组相互作用。

定量分析而非显著性检验： 与传统的4C方法不同，UMI-4C主要关注的是接触强度的定量分析，而不是检测显著的相互作用。

## UMI4Cats
[文档](https://pasquali-lab.github.io/UMI4Cats/articles/UMI4Cats.html)

fastq文件命名：condition_replicate_viewpoint

```R
library(UMI4Cats)
# 0、下载示例数据
path <- downloadUMI4CexampleData(out_dir = '/mnt/hpc/home/xuxinran/4C/UMI4C/test', verbose = TRUE, reduced = FALSE)

# 1、生成酶消化参考基因组
## 这里使用的是DpnII酶（其识别位点为GATC），cut_pos = 0表示在GATC识别位点的起始处切割(↓GATC)。
hg19_dpnii <- digestGenome(
    cut_pos = 0,
    res_enz = "GATC",
    name_RE = "DpnII",
    ref_gen = BSgenome.Hsapiens.UCSC.hg19::BSgenome.Hsapiens.UCSC.hg19,
    out_path = file.path("/mnt/hpc/home/xuxinran/4C/UMI4C/test", "digested_genome/")
)

# 2、处理fastq数据
contactsUMI4C(
    fastq_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/UMI4Cats_data/CIITA/fastq",
    wk_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir",
    bait_seq = "GGACAAGCTCCCTGCAACTCA",
    bait_pad = "GGACTTGCA",
    res_enz = "GATC",
    cut_pos = 0,
    digested_genome = hg19_dpnii,
    bowtie_index = "/mnt/hpc/home/xuxinran/REF/hg19/Sequence/Bowtie2Index/hg19",
    ref_gen = BSgenome.Hsapiens.UCSC.hg19::BSgenome.Hsapiens.UCSC.hg19,
    threads = 10
)
## file_pattern：可用于在“fastq_dir”中筛选想要分析的FastQ文件名的字符模式；没有的话就会分析文件夹下所有的数据
## bait_seq：viewpoint的序列
## bait_pad：引物与酶切位点之间的间隔填充物
```

顺序：bait_seq(viewpoint)-----bait_pad-----res_enz-----contact seq
在此处理步骤中，只选择包含bait_seq+bait_pad+res_enz的读取。平均Phread质量分数<20的阅读被过滤掉。
最终输出是存储在wk_dir/count压缩tsv文件，其中包含viewpoint-contact的坐标以及支持该特定交互的UMI数量

3、获取过滤和对齐统计信息:/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/logs/stats_summary.txt
- specific_reads/nonspecific_reads 包含bait_seq+bait_pad+res_enz的reads。
- filtered_reads/filtout_reads specific_reads中经过Phred quality scores >= 20过滤的read。
- al_mapped/al_unmapped 比对成功和失败的reads。
- umi 表示经过UMI去重后保留的独特分子。
```R
library(ggplot2)
plot <- statsUMI4C(wk_dir = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir")
ggsave(filename = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/statsUMI4C_plot.png", plot = plot, width = 8, height = 6)
```


```R
# 4、分析结果
files <- list.files(file.path("/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir", "count"), pattern = "*_counts.tsv.gz", full.names = TRUE) ## 获取所有的tsv文件
colData <- data.frame(
    sampleID = gsub("_counts.tsv.gz", "", basename(files)),
    file = files,
    stringsAsFactors = FALSE
)

library(tidyr)
colData <- colData %>%
    separate(sampleID, into = c("condition", "replicate", "viewpoint"), remove = FALSE) ## 根据sampleID拆分得到的数据情况，所以fastq命名的时候很重要！
umi <- makeUMI4C(
    colData = colData,
    viewpoint_name = "CIITA",
    bait_expansion = 2e6
)
## grouping：colData 中用于合并样本或重复实验的列名称。设置为 NULL 表示不进行合并。默认是 "condition"，意味着按条件分组。
## bait_exclusion：在viewpoint周围要排除的区域大小（以 bp 为单位）。默认是 3000 bp。
## bait_expansion：在viewpoint的上游和下游分析的区域大小（以 bp 为单位），默认是 1 Mb。
## scales：一个数值向量，用于计算域图（domainogram）。默认范围是 5:150，即从 5 到 150 个尺度。
```
处理内容：
1. 移除 bait 周围的片段末端，因为可能是线性距离近导致互作富集
解决方法：makeUMI4C 会自动移除 bait 附近的一些片段末端。默认情况下，移除范围为 bait 两侧的 3kb（bait_exclusion 参数）

1. 限定分析的基因组区域
为了减少计算复杂度并专注于感兴趣的区域，makeUMI4C 默认将分析限定在 bait 周围的 2Mb 范围内（即上下游各 1Mb 的区域（bait_expansion 参数），而不是整个基因组。这样可以确保分析的重点集中在与 bait 直接相关的区域。

1. 对同一组中的样本进行 UMI 计数的汇总
如果你有多个样本（例如对照组和处理组），你可能会将它们划分到不同的组中，来进行差异分析。在这种情况下，makeUMI4C 会对属于同一组的样本的 UMI（独特分子标记）计数进行汇总。(grouping 参数)

1. 获得用于标准化的归一化矩阵
为了保证不同样本或组之间的比较是合理的，makeUMI4C 通过归一化矩阵对每个组进行标准化处理。这些矩阵会根据每个组中的 UMI 总数进行比例缩放。默认情况下，样本或组中 UMI 总数最少的将作为标准化参考组。(normalized 参数默认True)

1. 为每个组计算 domainogram
它将不同尺度（即不同长度的窗口）中的 UMI 计数进行聚合，帮助你识别 bait 周围的相互作用区域和频率。
会根据设定的 scales 参数（默认为 5 到 150）计算 domainogram。它通过不同尺度聚合相互作用的 UMI 数据

1. 计算自适应趋势
自适应趋势用于平滑和优化相互作用信号，减少噪音的影响。对于每个组，makeUMI4C 会根据所定义的窗口和标准差（通过 sd 参数设置，默认值为 2）计算 UMI 的自适应趋势，以更清晰地展示 bait 与基因组其他区域的相互作用模式。

```R
# 5、获取UMI-4C分析中的各类数据(没啥用)
dgram(umi) # 返回每个样本的域图
dgram(groupsUMI4C(umi)$condition) # 返回按条件分组的域图
bait(umi) ## 返回viewpoint位置
trend(umi) ## 获取自适应平滑趋势，这个趋势图描述了染色质交互随距离变化的情况。
resultsUMI4C(umi) ## 获取差异分析的结果，前提是对UMI-4C对象已经进行过差异分析。它会输出差异交互区域的信息。
groupsUMI4C(umi)## 这个函数用于访问分组后的UMI-4C对象。在你的例子中，样本按 condition 变量进行分组，即分为 ctrl 和 cyt 两个条件。你可以使用 groupsUMI4C(umi)$<grouping-variable> 来访问分组后的对象。
head(assay(umi)) ## 获取原始UMI计数
head(assay(groupsUMI4C(umi)$condition)) ## 获取按条件分组的UMI计数
colData(umi) # 查看样本的元数据信息
rowRanges(umi) # 获取UMI-4C片段的坐标信息
```

6、识别UMI-4C分析中显著的染色质交互区域
1. 定义候选区域
在UMI-4C实验中，用户通常需要指定一组感兴趣的区域（例如增强子、开放染色质区域等），以便检测这些区域与viewpoint之间的交互。如果没有现成的候选区域，用户可以使用 makeWindowFragments() 函数，根据限制性酶片段生成一系列固定大小的窗口（这里 n_frags=8 表示每个窗口包含8个限制性酶片段的长度）。
```R
win_frags <- makeWindowFragments(umi, n_frags=8)
```

2. 调用交互检测函数
使用 callInteractions() 函数来检测UMI-4C实验中是否在指定的候选区域内观察到了显著的交互。
```R
gr <-  callInteractions(umi4c = umi,
                        design = ~condition,
                        query_regions = win_frags,
                        padj_threshold = 0.01,
                        zscore_threshold=2)
# design = ~condition：指定实验设计，这里是按照条件（condition）分组来检测不同组别间的交互差异。
# padj_threshold = 0.01：设定调整后的p值阈值，小于这个阈值的交互被认为是显著的。
# zscore_threshold=2：设定Z分数阈值，Z分数高于2的区域表明这些区域有显著交互。
```

3. 可视化交互
```R
all <- plotInteractionsUMI4C(umi, gr, grouping = NULL, significant=FALSE, xlim=c(10.75e6, 11.1e6))
sign <- plotInteractionsUMI4C(umi, gr, grouping = NULL, significant=TRUE, xlim=c(10.75e6, 11.1e6))
## grouping = NULL：未进行分组可视化。如果需要按条件或分组可视化，需指定分组变量。
## significant=FALSE：是否只显示显著的交互区域。FALSE 表示显示所有候选区域。
## xlim=c(10.75e6, 11.1e6)：设置X轴基因组坐标的显示范围，用于缩放显示指定区域。
```

4. 可视化
```R
# 同时有频率折线图和频率热图
library(ggplot2)
combined_plot <- cowplot::plot_grid(all, sign, ncol=2, labels=c("All", "Significant"))
ggsave(filename = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/combined_plot.png", plot = combined_plot, width = 15, height = 10)
# ncol=2：指定图像布局为2列。
# labels=c("All", "Significant")：为每个图像添加标签，分别为“全部”和“显著”。

# 只绘制其中一个
ggsave(filename = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/sign_plot.png", plot = sign, width = 8, height = 6)

# 只有频率折线图
plot <- plotUMI4C(umi,
    grouping = NULL,
    TxDb = TxDb.Hsapiens.UCSC.hg19.knownGene::TxDb.Hsapiens.UCSC.hg19.knownGene,
    dgram_plot = FALSE
)
ggsave(filename = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/plotUMI4C.png", plot = plot, width = 15, height = 10)
```

5. 提取显著交互
```R
inter <- getSignInteractions(gr)
```

7、差异分析
```R
# 样本数量充足 UMI 数量较高 实验设计较复杂
umi_wald <- waldUMI4C(umi,
                      query_regions = inter,
                      design = ~condition)

umi_fisher <- fisherUMI4C(umi,
                          grouping = "condition",
                          query_regions = inter,
                          filter_low = 20)

# 显示结果
res <- resultsUMI4C(umi_fisher, ordered = TRUE, counts = TRUE, format = "data.frame")
# 保存结果到 TSV 文件
write.table(res, file = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/results.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
# 保存结果到 CSV 文件
write.csv(res, file = "/mnt/hpc/home/xuxinran/4C/UMI4C/test/workdir/results.csv", row.names = FALSE)

# 结果绘图，上面是四个线 这里只有两个线
plotUMI4C(umi_fisher, grouping = "condition", xlim=c(10.75e6, 11.25e6), ylim=c(0,10))
```

结果
start；end：contact的起始和终止位置
id: contact的唯一ID。
mcols.position: 这个字段可能指的是该区域在分析中所属的某个特定位置或类型（如“upstream”）。
umis_ref；umis_cond: 这个contact分别在对照组和实验组中出现的次数吗
pvalue: contact在两组之间的统计显著性。
odds_ratio: 这个字段表示在条件组和参考组之间的优势比。
log2_odds_ratio: 这个字段表示优势比的对数值。
padj: 这个字段表示经过多重检验校正后的P值。。
sign: 该区域是否被认为是显著的。

# 实际运行问题
1. 首先是有可能酶和viewpoint离得很远，这里找到酶和viewpoint的位置 然后将酶上游15bp定为实际的viewpoint
2. 实际的数据中，有很多不是以viewpoint-酶开头的read，需要用/mnt/hpc/home/xuxinran/4C/UMI4C/get_viewpoint.py筛选一下
3. 筛选出来的read长度不统一，需要用/mnt/hpc/home/xuxinran/4C/UMI4C/flat_readlen.py统一read的长度，统一的长度就是所有一次性分析fastq中最短的read长度，最好不要小于70
