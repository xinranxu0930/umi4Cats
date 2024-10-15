R1，R2，R3，I1分别代表read 1，barcode，read 2 和 sample index

[CellRanger-ATAC定量](https://cloud.tencent.com/developer/article/2245873)

```shell
# 首先要改文件名
mv SRR16213608_1.fastq.gz   SRR16213608_S1_L001_I1_001.fastq.gz
mv SRR16213608_2.fastq.gz   SRR16213608_S1_L001_R1_001.fastq.gz
mv SRR16213608_3.fastq.gz   SRR16213608_S1_L001_R2_001.fastq.gz
mv SRR16213608_4.fastq.gz   SRR16213608_S1_L001_R3_001.fastq.gz
```

sh文件内容
```paint
bin=/mnt/hpc/home/xuxinran/softward/cellranger-atac-2.1.0/bin/cellranger-atac
db=/mnt/hpc/home/xuxinran/REF/hg19/hg19-scATAC-reference-sources/hg19
ls $bin; ls $db
fq_dir=/mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x
$bin count --id=$1 \
--localcores=50 \
--reference=$db \
--fastqs=$fq_dir \
--sample=$1
```

运行
```shell
bash 2x.sh scMicro-ATAC-2x 1>log-scMicro-ATAC-2x.txt 2>&1
bash 12x.sh scMicro-ATAC-12x 1>log-scMicro-ATAC-12x.txt 2>&1
```

[结果文件](https://mp.weixin.qq.com/s/_l_uYQjjIVXlGCiic7FsYQ)
[结果文件](https://mp.weixin.qq.com/s/C496e81tvw0Sjx9CAQ364w)

制作参考基因组
```shell
mkdir -p /mnt/hpc/home/xuxinran/REF/hg19/hg19-scATAC-reference-sources

wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz
wget http://ftp.ensembl.org/pub/release-75/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz
# motif
wget https://jaspar.elixir.no/download/data/2024/CORE/JASPAR2024_CORE_non-redundant_pfms_jaspar.txt

# 修改fa文件
# >1 dna:chromosome chromosome:GRCh37:1:1:249250621:1 REF
# >chr1 1
fasta_in="Homo_sapiens.GRCh37.75.dna.primary_assembly.fa"
fasta_modified="Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.modified"
cat "$fasta_in" \
    | sed -E 's/^>(\S+).*/>\1 \1/' \
    | sed -E 's/^>([0-9]+|[XY]) />chr\1 /' \
    | sed -E 's/^>MT />chrM /' \
    > "$fasta_modified"


# 修改gtf文件
#     ... gene_id "ENSG00000223972.5"; ...
#     ... gene_id "ENSG00000223972"; gene_version "5"; ...
ID="(ENS(MUS)?[GTE][0-9]+)\.([0-9]+)"
gtf_in="gencode.v19.annotation.gtf"
gtf_modified="gencode.v19.annotation.gtf.modified"
cat "$gtf_in" \
    | sed -E 's/gene_id "'"$ID"'";/gene_id "\1"; gene_version "\3";/' \
    | sed -E 's/transcript_id "'"$ID"'";/transcript_id "\1"; transcript_version "\3";/' \
    | sed -E 's/exon_id "'"$ID"'";/exon_id "\1"; exon_version "\3";/' \
    > "$gtf_modified"

BIOTYPE_PATTERN=\
"(protein_coding|lncRNA|\
IG_C_gene|IG_D_gene|IG_J_gene|IG_LV_gene|IG_V_gene|\
IG_V_pseudogene|IG_J_pseudogene|IG_C_pseudogene|\
TR_C_gene|TR_D_gene|TR_J_gene|TR_V_gene|\
TR_V_pseudogene|TR_J_pseudogene)"
GENE_PATTERN="gene_type \"${BIOTYPE_PATTERN}\""
TX_PATTERN="transcript_type \"${BIOTYPE_PATTERN}\""
READTHROUGH_PATTERN="tag \"readthrough_transcript\""
PAR_PATTERN="tag \"PAR\""
cat "$gtf_modified" \
    | awk '$3 == "transcript"' \
    | grep -E "$GENE_PATTERN" \
    | grep -E "$TX_PATTERN" \
    | grep -Ev "$READTHROUGH_PATTERN" \
    | grep -Ev "$PAR_PATTERN" \
    | sed -E 's/.*(gene_id "[^"]+").*/\1/' \
    | sort \
    | uniq \
    > "./gene_allowlist"


# Filter the GTF file based on the gene allowlist
gtf_filtered="gencode.v19.annotation.gtf.filtered"
# Copy header lines beginning with "#"
grep -E "^#" "$gtf_modified" > "$gtf_filtered"
# Filter to the gene allowlist
grep -Ff "gene_allowlist" "$gtf_modified" >> "$gtf_filtered"


# Change motif headers so the human-readable motif name precedes the motif
# identifier. So ">MA0004.1    Arnt" -> ">Arnt_MA0004.1".
motifs_modified="JASPAR2024_CORE_non-redundant_pfms_jaspar.txt.modified"
awk '{
    if ( substr($1, 1, 1) == ">" ) {
        print ">" $2 "_" substr($1,2)
    } else {
        print
    }
}' "JASPAR2024_CORE_non-redundant_pfms_jaspar.txt" > "$motifs_modified"


# Create a config file
config_in="./config"
echo """{
    organism: \"Homo_sapiens\"
    genome: [\""hg19"\"]
    input_fasta: [\""$fasta_modified"\"]
    input_gtf: [\""$gtf_filtered"\"]
    input_motifs: \""$motifs_modified"\"
    non_nuclear_contigs: [\"chrM\"]
}""" > "$config_in"


# Create reference package
/mnt/hpc/home/xuxinran/softward/cellranger-atac-2.1.0/bin/cellranger-atac mkref --ref-version="2023" --config="$config_in"
```