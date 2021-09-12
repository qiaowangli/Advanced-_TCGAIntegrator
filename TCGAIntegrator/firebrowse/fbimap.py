
# This is the initial (internal) state used to map names/types/params to
# generated bindings.  It will be augmented with additional content during
# code generation, then written to fbmap.py for runtime use in the bindings.

# Make client bindings more digestible with shorter names for some REST params
ParamAliases = {
    # These shrink bindings signatures by using shorter param names
    'tcga_participant_barcode' : 'barcode',
    'cde_name' : 'cde',
    'fh_cde_name' : 'fh_cde',

    # And these allow shorter param names to be used at CLI
    'barcode' : 'tcga_participant_barcode',
    'cde' : 'cde_name',
    'fh_cde' : 'fh_cde_name',
}

# The fbHLMap dict serves two purposes:
#   - helps translate the low-level FireBrowse RESTful api bindings to
#     "more Pythonic" higher-level equivalents, with simpler calling
#     conventions & defaults tuned to biologist use cases (e.g. return
#     TSV, all pages, etc)
#   - provides a lookup table so that the high level functions can
#     be easily identified, called, listed, etc in the CLI use case

fbHLMap = {  # {{{
"Samples.mRNASeq" : { 'name' : "mrnaseq" },
"Samples.miRSeq" : { 'name' : "mirseq" },
"Samples.Clinical" : { 'name' : "clinical" },
"Samples.Clinical_FH" : { 'name' : "clinical_fh" },
"Analyses.MutationMAF" : { 'name' : "maf" },
"Analyses.MutationSMG" : { 'name' : "smg" },
"Analyses.CopyNumberGenesAll" : { 'name' : "cn_genes_all" },
"Analyses.CopyNumberGenesFocal" : { 'name' : "cn_genes_focal" },
"Analyses.CopyNumberGenesThresholded" : { 'name' : "cn_levels" },
"Analyses.CopyNumberGenesAmplified" : { 'name' : "cn_genes_amp" },
"Analyses.CopyNumberGenesDeleted" : { 'name' : "cn_genes_del" },
"Analyses.mRNASeqQuartiles" : { 'name' : "mrnaseq_quartiles" },
"Analyses.Reports" : { 'name' : "reports" },
"Analyses.FeatureTable" : { 'name' : "featuretable" },
"Archives.StandardData": { 'name' : "stddata" },
"Metadata.Centers" : { 'name' : "centers" },
"Metadata.ClinicalNames" : { 'name' : "clinical_names" },
"Metadata.ClinicalNames_FH" : { 'name' : "clinical_names_fh" },
"Metadata.Cohort" : { 'name' : "cohort" },
"Metadata.Cohorts" : { 'name' : "cohorts" },
"Metadata.Counts" : { 'name' : "counts" },
"Metadata.Dates" : { 'name' : "dates" },
"Metadata.HeartBeat" : { 'name' : "heartbeat" },
"Metadata.MAFColNames" : { 'name' : "maf_colnames" },
"Metadata.Patients" : { 'name' : "patients" },
"Metadata.Platforms" : { 'name' : "platforms" },
"Metadata.SampleTypes" : { 'name' : "sampletypes" },
"Metadata.SampleTypeBarcode" : { 'name' : "barcode2type" },
"Metadata.SampleTypeCode" : { 'name' : "samplecode2type" },
"Metadata.SampleTypeShortLetterCode" : { 'name' : "sampletype2code" },
}  # }}}
