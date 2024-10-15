from subprocess import call, check_output
from collections import Counter
import pandas as pd
import mappy as mp
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.serif"] = "Arial" # Matplotlib图形的字体
mpl.rcParams["pdf.fonttype"] = 42 # 输出PDF文件时的字体类型
mpl.use("Agg") #Agg 渲染器是非交互式的后端，没有GUI界面，所以不显示图片，它是用来生成图像文件。Qt5Agg 是意思是Agg渲染器输出到Qt5绘图面板，它是交互式的后端，拥有在屏幕上展示的能力


def parse_args():
    parser = argparse.ArgumentParser(description="UMI Duplication")
    parser.add_argument("-l", "--umi_len", type=int, default=20, help="UMI length")
    parser.add_argument("-1", "--fq1", type=str, required=True, help="Read1 fastq")
    parser.add_argument("-2", "--fq2", type=str, default=None, help="Read2 fastq")
    parser.add_argument(
        "-o", "--outprefix", type=str, required=True, help="Output prefix"
    )
    return parser.parse_args()


def count_umis(sample, fq1, fq2=None, umi_len=20):
    umis = {}
    if fq2 is None:
        for read1 in mp.fastx_read(fq1):
            umi = read1[1][:umi_len]
            umis[umi] = umis.get(umi, 0) + 1
    else:
        for read1, read2 in zip(mp.fastx_read(fq1), mp.fastx_read(fq2)):
            umi = "-".join(sorted([read1[1][:umi_len], read2[1][:umi_len]]))
            umis[umi] = umis.get(umi, 0) + 1

    umi_counts = Counter(umis.values()) # Counter({'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1})
    umi_counts = sorted(umi_counts.items(), key=lambda x: x[0]) #[('a', 5), ('b', 4), ('c', 3), ('d', 2), ('e', 1)]
    with open(f"./{sample}_hist.txt", "w") as f:
        for k, v in umi_counts:
            f.write(f"{k}\t{v}\n")


def run_preseq(sample):
    res = check_output("which preseq", shell=True)
    if res == b"":
        raise Exception("preseq is not installed")

    call(
        f"preseq c_curve -H -o ./{sample}_c_curve.txt ./{sample}_hist.txt",
        shell=True,
    )

    call(
        f"preseq lc_extrap -D -H -o ./{sample}_lc_extrap.txt ./{sample}_hist.txt",
        shell=True,
    )


def plot_complexity(sample):
    c_curve = pd.read_csv(f"./{sample}_c_curve.txt", sep="\t")
    lc_extrap = pd.read_csv(f"./{sample}_lc_extrap.txt", sep="\t")

    fig, ax = plt.subplots(figsize=(8, 4))
    lc_extrap["TOTAL_READS"] = lc_extrap["TOTAL_READS"] / 1e6
    lc_extrap["EXPECTED_DISTINCT"] = lc_extrap["EXPECTED_DISTINCT"] / 1e6
    c_curve["total_reads"] = c_curve["total_reads"] / 1e6
    c_curve["distinct_reads"] = c_curve["distinct_reads"] / 1e6
    lc_extrap["slope"] = lc_extrap["EXPECTED_DISTINCT"] - lc_extrap[
        "EXPECTED_DISTINCT"
    ].shift(1)
    xlim = 10 * c_curve["total_reads"].max()
    # ylim = 10 * c_curve["distinct_reads"].max()
    ax.plot(lc_extrap["TOTAL_READS"], lc_extrap["EXPECTED_DISTINCT"], label="Predicted")
    ax.plot(c_curve["total_reads"], c_curve["distinct_reads"], label="Current")
    ax.plot([0, xlim / 2], [0, xlim / 2], "k--")
    annotate_text = f"Current Slope: {lc_extrap['slope'].loc[len(c_curve)]:.2g}\n"
    for amount in [10, 50, 100, 200]:
        annotate_text += f"{amount}M Slope: {lc_extrap['slope'].loc[amount]:.2g}\n"
    ax.annotate(
        annotate_text,
        xy=(0.95, 0.95),
        xycoords="axes fraction",
        ha="right",
        va="top",
        fontsize=10,
    )
    ax.set_xlim(-xlim / 30, xlim)
    ax.set_ylim(-xlim / 1.5 / 30, xlim / 1.5)
    ax.set_xlabel("Total UMIs (M)")
    ax.set_ylabel("Distinct UMIs (M)")
    ax.set_title(f"UMI Complexity Curve ({sample})")
    ax.legend(loc="upper left")
    fig.savefig(f"./{sample}_duplication.pdf", bbox_inches="tight")
    # os.remove(f'./{sample}_c_curve.txt')
    # os.remove(f'./{sample}_lc_extrap.txt')
    os.remove(f"./{sample}_hist.txt")


def main():
    args = parse_args()
    count_umis(args.outprefix, args.fq1, args.fq2, args.umi_len)
    run_preseq(args.outprefix)
    plot_complexity(args.outprefix)


if __name__ == "__main__":
    main()
