# H3K27ac:Peak-to-All 去122
export PATH="/f/xinran/MicroC/HiC-Pro_3.1.0/bin/:$PATH"
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C config.txt

bamCoverage -b GM_HiChIP_H3K27ac_biological_mapped_f.bam -of bedgraph -p 36 -o GM_HiChIP_H3K27ac_biological.coverage.bedgraph

## R画图
# 先筛MCUT-merge.interactions_FitHiC_Q0.01.bed
library(Sushi)

cov <- read.table("/f/xinran/11111/GM-H3K27ac.coverage.bedgraph")
arc <- read.table("/f/xinran/11111/GM_fithichip/fithichip_res/FitHiChIP_Peak2ALL_b5000_L1000_U2000000/P2PBckgr_0/Coverage_Bias/FitHiC_BiasCorr/GM-H3K27ac.interactions_FitHiC_paint.bed", header=TRUE)
arc$dist <- abs(arc$e2 - arc$s1)

chrom = "chr1"
# chromstart = 1070000
# chromend = 5495000
chromstart = 23850000
chromend = 23965000

pdfname <- "/f/xinran/11111/GM.chr1_2.pdf"
makepdf = TRUE
if(makepdf==TRUE)
      {
      pdf(pdfname , height=10, width=12)
      }

##set layout
layout(matrix(c(1,
      2
      ), 2,1, byrow=TRUE))
par(mgp=c(3,.3,0))

##plot coverage
par(mar=c(3,4,2,2))
plotBedgraph(cov,chrom,chromstart,chromend)
labelgenome(chrom,chromstart,chromend,n=4,scale="Mb")
mtext("Read Depth",side=2,line=1.75,cex=1,font=2)
axis(side=2,las=2,tcl=.2)

##plot arcs with height based on contact frequency
par(mar=c(3,4,2,2))
plotBedpe(arc,chrom,chromstart,chromend,heights = arc$dist,plottype="loops", flip=TRUE)
labelgenome(chrom, chromstart,chromend,side=3, n=3,scale="Mb")
axis(side=2,las=2,tcl=.2)
mtext("distance",side=2,line=1.75,cex=.75,font=2)

if (makepdf==TRUE)
{
dev.off()
}
