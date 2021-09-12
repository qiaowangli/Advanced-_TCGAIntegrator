
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
