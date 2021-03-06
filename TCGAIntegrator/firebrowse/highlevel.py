#!/usr/bin/env python

# This file is part of fbget: Python wrappers for the firebrowse RESTful api
# Autogenerated on 2017_10_31 21:27:19 EDT

__version__ = '0.1.11'

# Copyright (c) 2015-2016, Broad Institute, Inc. {{{
# All rights reserved.
#
# This file is part of fbget: Python wrappers for the FireBrowse RESTful api
#
# FBGET is distributed under the following BSD-style license:
#
# Copyright (c) 2015-2017, Broad Institute, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the Broad Institute, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS."  BROAD MAKES NO EXPRESS OR IMPLIED
# REPRESENTATIONS OR WARRANTIES OF ANY KIND REGARDING THE SOFTWARE AND
# COPYRIGHT, kINCLUDING, BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, CONFORMITY WITH ANY DOCUMENTATION,
# NONINFRINGEMENT, OR THE ABSENCE OF LATENT OR OTHER DEFECTS, WHETHER OR NOT
# DISCOVERABLE. IN NO EVENT SHALL BROAD, THE COPYRIGHT HOLDERS, OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF,
# HAVE REASON TO KNOW, OR IN FACT SHALL KNOW OF THE POSSIBILITY OF SUCH DAMAGE.
#
# If, by operation of law or otherwise, any of the aforementioned warranty
# disclaimers are determined inapplicable, your sole remedy, regardless of the
# form of action, including, but not limited to, negligence and strict
# liability, shall be replacement of the software with an updated version if
# one exists.
#
# In addition, FBGET is distributed, in part, under and subject to the
# provisions of licenses for:
#
#   Python requests library
#   (http://docs.python-requests.org/en/latest/user/intro),
#   Copyright (c) 2015 Kenneth Reitz (all rights reserved); and

#   Python 2.7.9
#   (https://docs.python.org/3/license.html),
#   Copyright (c) 2001-2015 Python Software Foundation (all rights reserved).
#
# Development of FBGET has been funded in whole or in part with federal funds
# from the National Institutes of Health, Department of Health and Human
# Services, under Grant No. U24 CA143845-03.
#
# }}}

import os
import sys
import argparse
import __builtin__

from firebrowse import *
set_basepath("http://firebrowse.org/api")

# Stop Python from complaining when I/O pipes are closed
if os.name == 'posix':
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE, SIG_DFL)

__Samples = Samples(format=CODEC_TSV, page=PAGES_ALL)

@hlwrap("Samples.mRNASeq")
def mrnaseq(gene=None, **kwargs):
    '''
    High level wrapper for the firebrowse Samples.mRNASeq method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Samples.mRNASeq(gene=gene,**kwargs)

@hlwrap("Samples.miRSeq")
def mirseq(mir=None, **kwargs):
    '''
    High level wrapper for the firebrowse Samples.miRSeq method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Samples.miRSeq(mir=mir,**kwargs)

@hlwrap("Samples.Clinical")
def clinical(cohort=None, barcode=None, cde=None, **kwargs):
    '''
    High level wrapper for the firebrowse Samples.Clinical method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Samples.Clinical(cohort=cohort,barcode=barcode,cde=cde,**kwargs)

@hlwrap("Samples.Clinical_FH")
def clinical_fh(cohort=None, barcode=None, fh_cde=None, **kwargs):
    '''
    High level wrapper for the firebrowse Samples.Clinical_FH method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Samples.Clinical_FH(cohort=cohort,barcode=barcode,fh_cde=fh_cde,**kwargs)

__Analyses = Analyses(format=CODEC_TSV, page=PAGES_ALL)

@hlwrap("Analyses.MutationMAF")
def maf(cohort=None, gene=None, barcode=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.MutationMAF method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.MutationMAF(cohort=cohort,gene=gene,barcode=barcode,**kwargs)

@hlwrap("Analyses.MutationSMG")
def smg(cohort=None, gene=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.MutationSMG method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.MutationSMG(cohort=cohort,gene=gene,**kwargs)

@hlwrap("Analyses.CopyNumberGenesAll")
def cn_genes_all(gene=None, barcode=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.CopyNumberGenesAll method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.CopyNumberGenesAll(gene=gene,barcode=barcode,**kwargs)

@hlwrap("Analyses.CopyNumberGenesFocal")
def cn_genes_focal(gene=None, barcode=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.CopyNumberGenesFocal method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.CopyNumberGenesFocal(gene=gene,barcode=barcode,**kwargs)

@hlwrap("Analyses.CopyNumberGenesThresholded")
def cn_levels(gene=None, barcode=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.CopyNumberGenesThresholded method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.CopyNumberGenesThresholded(gene=gene,barcode=barcode,**kwargs)

@hlwrap("Analyses.CopyNumberGenesAmplified")
def cn_genes_amp(cohort=None, gene=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.CopyNumberGenesAmplified method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.CopyNumberGenesAmplified(cohort=cohort,gene=gene,**kwargs)

@hlwrap("Analyses.CopyNumberGenesDeleted")
def cn_genes_del(cohort=None, gene=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.CopyNumberGenesDeleted method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.CopyNumberGenesDeleted(cohort=cohort,gene=gene,**kwargs)

@hlwrap("Analyses.mRNASeqQuartiles")
def mrnaseq_quartiles(gene, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.mRNASeqQuartiles method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.mRNASeqQuartiles(gene,**kwargs)

@hlwrap("Analyses.Reports")
def reports(**kwargs):
    '''
    High level wrapper for the firebrowse Analyses.Reports method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.Reports(**kwargs)

@hlwrap("Analyses.FeatureTable")
def featuretable(cohort=None, **kwargs):
    '''
    High level wrapper for the firebrowse Analyses.FeatureTable method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Analyses.FeatureTable(cohort=cohort,**kwargs)

__Archives = Archives(format=CODEC_TSV, page=PAGES_ALL)

@hlwrap("Archives.StandardData")
def stddata(**kwargs):
    '''
    High level wrapper for the firebrowse Archives.StandardData method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Archives.StandardData(**kwargs)

__Metadata = Metadata(format=CODEC_TSV, page=PAGES_ALL)

@hlwrap("Metadata.Centers")
def centers(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.Centers method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.Centers(**kwargs)

@hlwrap("Metadata.ClinicalNames")
def clinical_names(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.ClinicalNames method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.ClinicalNames(**kwargs)

@hlwrap("Metadata.ClinicalNames_FH")
def clinical_names_fh(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.ClinicalNames_FH method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.ClinicalNames_FH(**kwargs)

@hlwrap("Metadata.Cohorts")
def cohorts(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.Cohorts method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.Cohorts(**kwargs)

@hlwrap("Metadata.Counts")
def counts(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.Counts method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.Counts(**kwargs)

@hlwrap("Metadata.Dates")
def dates(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.Dates method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.Dates(**kwargs)

@hlwrap("Metadata.HeartBeat")
def heartbeat(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.HeartBeat method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.HeartBeat(**kwargs)

@hlwrap("Metadata.MAFColNames")
def maf_colnames(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.MAFColNames method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.MAFColNames(**kwargs)

@hlwrap("Metadata.Patients")
def patients(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.Patients method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.Patients(**kwargs)

@hlwrap("Metadata.Platforms")
def platforms(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.Platforms method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.Platforms(**kwargs)

@hlwrap("Metadata.SampleTypes")
def sampletypes(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.SampleTypes method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.SampleTypes(**kwargs)

@hlwrap("Metadata.SampleTypeBarcode")
def barcode2type(TCGA_Barcode, **kwargs):
    '''
    High level wrapper for the firebrowse Metadata.SampleTypeBarcode method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.SampleTypeBarcode(TCGA_Barcode,**kwargs)

@hlwrap("Metadata.SampleTypeCode")
def samplecode2type(code, **kwargs):
    '''
    High level wrapper for the firebrowse Metadata.SampleTypeCode method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.SampleTypeCode(code,**kwargs)

@hlwrap("Metadata.SampleTypeShortLetterCode")
def sampletype2code(short_letter_code, **kwargs):
    '''
    High level wrapper for the firebrowse Metadata.SampleTypeShortLetterCode method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.SampleTypeShortLetterCode(short_letter_code,**kwargs)

@hlwrap("Metadata.TSSites")
def tssites(**kwargs):
    '''
    High level wrapper for the firebrowse Metadata.TSSites method.
    By default it returns ALL pages of data, in TSV format.
    '''
    return __Metadata.TSSites(**kwargs)

fbHLMap["param_names"] = param_names
fbHLMap["param_values"] = param_values
fbHLMap["help"] = help
fbHLMap["client_version"] = client_version

def func_examples():
    import pydoc
    examples = '''
    # Every line of these examples can be cut and directly pasted to your
    # UNIX-like command line.  Comments will be ignored, while everything
    # not beginning with the # comment character will be executed, as long
    # as fbget is in your $PATH

    # Get the RNASeq expression level of the POLE gene, for all TCGA samples
    # (both tumors and normals, in RSEM form, saved to file)
    fbget --outfile=fbget-test-pole.tsv mrnaseq pole

    # Similar query, but constrained to just the DLBC disease cohort
    fbget mrnaseq pole cohort=dlbc

    # Now constrained to single patient, and showing case insensitivity
    fbget mrnaseq pOlE baRcOdE=TCGA-RQ-A6JB

    # List all the disease cohorts offered by FireBrowse (note that aggregate
    # cohorts like COADREAD,KIPAN,GBMLGG,STES are not available at the TCGA DCC)
    fbget cohorts

    # Display help (docstring) for the function which retrieves clinical data
    fbget help clinical_fh

    # Calling functions with no arguments also displays help (docstring)
    fbget clinical_fh

    # Now get some actual clinical data, but only for 9 thyroid (THCA) cases,
    # and remove (cut) the date fields as an example of additional processing
    fbget clinical_fh barcode=TCGA-EL-A3MZ,TCGA-EL-A3MY,TCGA-EL-A3MX,TCGA-EL-A3MW,TCGA-EL-A3D4,TCGA-EL-A3D5,TCGA-EL-A3D6,TCGA-EL-A3D0,TCGA-EL-A3D1 | head -10 | cut -f1,2,7-

    # Display the complete list of clinical data element names (CDEs)
    fbget clinical_names_fh

    # List the functions may be called through fbget (-l does the same thing)
    fbget --list

    # Get 10 most significantly mutated ovarian cancer genes (and elide date)
    fbget smg OV rank=10 | cut -f4 --complement

    # Union of the names of parameters admitted by any FireBrowse function
    fbget param_names

    # Show the kinds of values that may be supplied via the cohort parameter
    # (applies to any function which admits the cohort parameter)
    fbget param_values cohort

    # Ditto, for the barcode and clinical data element (CDE) names
    fbget param_values barcode
    fbget param_values fh_cde

    # The documentation for param_values is helpful in its own right, too
    fbget help param_values

    # Levels of copy number alteration in TERT gene for 3 disease cohorts,
    # as computed by GISTIC2, redirected to file
    fbget cn_levels tert cohort=acc,KICH,LaMl,UCS > fbget-test-tert-cn.tsv

    # Which genes had significant copy number deletion (per GISTIC2 q values)
    # in BRCA & UCEC cohorts? (alternate method of saving to file, CLI option)
    fbget --outfile=fbget-test-cn-del.tsv cn_genes_del cohort=BRCA,ucec

    # Retrieve mature strand microRNASeq from UVM, as CSV (and again cut out the
    # dates--which also simplifies regression testing with new data releases)
    fbget mirseq hsa-let-7b-5p cohort=uvm format=csv | cut --complement -d, -f7

    # Repeat the same call to show that bogus parameters induce failure
    fbget mirseq has-let-7b-5p cohort=uvm format=Dum_De_Dum_Dumb
    '''
    pydoc.pager(examples)
    sys.exit(0)

def func_list():
    for name, value in sorted(fbHLMap.items()):
        if callable(value):
            print "    ",name
    sys.exit(0)

def func_docs(funcs=[]):
    # Emit documentation for one or more high-level functions
    if not funcs:
        funcs = sorted(fbHLMap.keys())
    for name in funcs:
        func = fbHLMap.get(name, None)
        if not func:
            print "ERROR: %s does not exist or is not callable here" % name
        elif callable(func):
            help(func)
    sys.exit(0)

def func_call(name, args):

    if name.lower() == 'help':
        if args:
            func_docs(args)
        else:
            main(argv=['-h'])

    func = fbHLMap.get(name, None)
    if not callable(func):
        print "ERROR: %s does not exist or is not callable here" % name
        return

    positional_args = []
    keyword_args = {}
    for arg in args:
        arg = arg.split('=')
        if len(arg) == 2:
            keyword_args[arg[0].lower()] = arg[1]
        else:
            positional_args.append(arg[0])

    try:
        result = func( *tuple(positional_args), **keyword_args)
    except Exception as e:
        print "Caught exception:",e.__class__.__name__," : ",e
        result = None

    if result:
        sys.stdout.write(result)
        sys.stdout.flush()

def main(argv=None):

    if argv:
        sys.argv.extend(argv)

    docs  = 'Python & UNIX CLI wrappers for the FireBrowse RESTful API\n'
    docs += '\nfbget simplifies use and extends the power of FireBrowse, by\n'
    docs += 'providing: low- and high-level Python wrappers to its RESTful\n'
    docs += 'API; an interface through which the high level functions may be\n'
    docs += 'called directly from the UNIX command line, without writing any\n'
    docs += 'Python code; and enabling the results of such to be immediately\n'
    docs += 'streamed to UNIX tools for further processing or analysis.  In\n'
    docs += 'addition, both the fbget CLI tool and the high level wrappers\n'
    docs += 'will by default retrieve all pages of data returned by the\n'
    docs += 'FireBrowse RESTful API, in TSV form that is most commonly used\n'
    docs += 'for bioinformatics analysis.\n'
    docs += '\nFor more information visit http://firebrowse.org\n'

    # Optional arguments
    parser = argparse.ArgumentParser(description=docs,
                formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--docs', action="store_true",default=False,
                help='emit documentation for entire api')
    parser.add_argument('-e', '--examples', action="store_true",default=False,
                help='show usage examples')
    parser.add_argument('-l', '--list', action="store_true", default=False,
                help='list all callable functions')
    #parser.add_argument('-m', '--mock', action="store_true", default=False,
    #            help="mock (dry-run): display the REST call that would be "\
    #                 "made for a given function, but don't actually issue it")
    parser.add_argument('-o', '--outfile', default=None, help="Specify "\
                'output file (will be overwritten if already exists) [sys.stdout]')
    parser.add_argument('-p', '--page_size', default=get_page_size(), type=int,
                help='change the page size requested by client [%(default)s]')
    parser.add_argument('-s', '--server', default=get_basepath(),
                help='Override remote API [%(default)s]. The '\
                'value of SERVER may be a simple name (e.g. "fbdev") of the '\
                'remote server, provided it offers the API at the canonical '\
                'paths, i.e. where the API is defined at '\
                'http://<server>/api/api-docs/ and calls are made to '\
                'http://<server>/api/<version>/<API_endpoint>. If your server '\
                'uses https or non-canonical paths, then SERVER must fully '\
                'specify <protocol>://<server>/<path>')
    parser.add_argument('-V', '--verbose', action='store_true',
                help='emit to stderr the RESTful calls made, etc [False]')
    parser.add_argument('-v', '--version', action='version',
                version='v%s' % __version__)

    # Positional (required) argument(s)
    parser.add_argument('function', nargs='?',
                help='name of the function to be called')
    parser.add_argument('arg', default=None, nargs='*',
                    help='arguments to pass to function')

    cli = parser.parse_args()

    # Handle options which perform utility tasks then exit
    if cli.list:
        func_list()
    elif cli.examples:
        func_examples()
    elif cli.docs:
        func_docs()

    # Handle options which alter the default behavior
    set_page_size(cli.page_size)

    if cli.outfile:
        sys.stdout = open(cli.outfile, "w")

    if cli.server != get_basepath():
        set_basepath(cli.server)

    set_verbosity(cli.verbose)

    if not cli.function:
        parser.error(' function name required when no -e | -h | -l options\n'\
                     '\tgiven; use -l or --list to see available functions')

    func_call(cli.function, cli.arg)

if __name__ == "__main__":
    try:
        status = main()
    except KeyboardInterrupt:
        status = 0
    sys.exit(status)
