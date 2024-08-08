- H0: 该区域没有与任何特征相关的因果变异
- H1: 该区域只有与特征1相关的因果变异
- H2: 该区域只有与特征2相关的因果变异
- H3: 该区域有与特征1和特征2分别相关的不同因果变异
- H4: 该区域有一个同时与特征1和特征2相关的共同因果变异
- PP.H0 + PP.H1 + PP.H2 + PP.H3 + PP.H4 = 1

[post-GWAS：使用coloc进行共定位分析](https://www.cnblogs.com/chenwenyan/p/15041963.html)

QTL二分类表型数据：rsID traitID pvalue beta

QTL连续性表型数据：
- rsID pvalue sdY
- rsID pvalue beta varbeta N MAF
- rsID pvalue MAF


```r
gwas <- read.table(file="E:/path_to_GWAS/GWAS.txt", header=T);
eqtl <- read.table(file="E:/path_to_eqtl/eQTL.txt", header=T);

# 合并两个输入数据
input <- merge(eqtl, gwas, by="rs_id", all=FALSE, suffixes=c("_eqtl","_gwas"))

# 共定位分析
result <- coloc.abf(dataset1=list(pvalues=input$pval_nominal_gwas, type="cc", s=0.33, N=50000), dataset2=list(pvalues=input$pval_nominal_eqtl, type="quant", N=10000), MAF=input$maf)
## dataset1的type="cc"指的是GWAS的表型是二分类（case和control）；
## dataset2的type="quant"指的是eQTL的表型（基因表达量）是连续型
## N指样本量；

# 筛选共定位的位点,这里假定后验概率大于0.95为共定位位点,只能同结果的pvalue找到这个点的rsID
library(dplyr)
need_result=result$results %>% filter(SNP.PP.H4 > 0.95)
```