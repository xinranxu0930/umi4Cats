import pandas as pd
import pysam
import numpy as np
import glob

pairtools_res = "no-GM-K27ac-2_L7_G028_valid_id.txt"
o = "no-GM-K27ac-2_L7_G028_dis.csv"
sam_files = glob.glob("no-GM-K27ac-2_L7_G028_aligned_ligation_sort_tmp.bam")

df = pd.read_csv(pairtools_res,sep="\t",header=None)
df.columns = ["readID","chrom1","s1","chrom2","s2","strand1","strand2"]
df['e1'] = np.nan
df['e2'] = np.nan
df.set_index('readID', inplace=True)
for sam in sam_files:
    samfile = pysam.AlignmentFile(sam, 'r',threads=4)
    for read in samfile:
        readid = read.query_name
        if readid in df.index:
            start = read.reference_start
            end = read.reference_end
            if df.loc[readid, 's1'] == start+1:
                df.loc[readid, 'e1'] = end+1
df = df.dropna(subset=['e1'])
df['dis'] = df['s2']-df['e1']
df.to_csv(o,header=None)