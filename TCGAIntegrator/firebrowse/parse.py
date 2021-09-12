
@autohelp(False)
def param_values(name):
    '''
    For the given named API parameter, indicate the values it may
    hold.  Most parameters are case insensitive (e.g. gene, cohort,
    TCGA barcode, tool), but some are not (e.g. column names in a
    MAF).  A parameter which admits multiple values (e.g. the gene of
    interest in mRNASeq expression samples) may be specified as a

        string     with values delimited by commas or whitespace
    OR
        sequence (e.g. list, tuple, set) of strings

    The api defines 'optionality' as the degree of 'required-ness' that
    a parameter possesses within a given signature: it may be one of

        required:   (mandatory) every required param must be specified
                    for each call, in positional form only.  There are
                    only a few of these exposed by the API.
    semiRequired:   at least one of set of semi-Required parameters, if
                    any, must be specified for each call; they may be
                    given in either positional or keyword form;  the
                    documentation for both the RESTful api and the Python
                    client bindings lists the semiRequired paramters.
        optional:   may always be omitted from any call

    Recall that in Python positional parameters MUST ALWAYS be specified
    first in the argument list, in exactly the order shown in the
    documentation.  Keyword arguments may appear in any order, as long as
    they ALL appear AFTER any of the required args.  Finally, note that
    "self" and "kwargs" are transparently inserted by Python at runtime,
    so you SHOULD NOT specify them explicitly in your calls.
    '''

    param = SupportedParameters.get(name, None)
    if not param:
        print "No such parameter '%s' is supported by the FireBrowse api" % name
        return

    values = ", ".join(param["values"])
    values = "The %s parameter may take the values:  %s" % (name, values)
    print values
    d = param["default"]

    # When list of values is long, e.g. tier1_cde_name, add whitespace
    if len(values) > 80:
        print

    if d:
        print "When not specified in an api call, its default value will be: ",d
    else:
        print "There is no default value for this parameter."

@autohelp(False)
def param_multivalued(name):
    ''' Does given named param permit >1 value to be specified?'''
    return SupportedParameters[name]["multiValued"]

def param_names():
    ''' List the names of all parameters offered by the API '''
    return (', '.join(SupportedParameters.keys())) + '\n'

def parse_args(args, argspec):
    # Partition the set of args passed to the calling Python function into
    #   restParams:   params array sent to RESTful api call on server
    #   clientParams: params dict passed to client func that issues RESTful call

    restParams = []
    clientParams = {}

    # Merge keyword (optional) args, if any, and positional (required) args
    kwargs = args.pop("kwargs", None)
    if kwargs:
        args.update(kwargs)

    # Respect defaults of containing object, for parameters that were omitted
    if "format" in argspec.queryParams and "format" not in args:
        args["format"] = argspec.caller.default_format

    if "page" in argspec.queryParams and "page" not in args:
        args["page"] = argspec.caller.default_page

    if "page_size" in argspec.queryParams and "page_size" not in args:
        args["page_size"] = get_page_size()

    # Elide anything else that should NOT be mistaken for a REST or client param
    args.pop("self", None)

    def normalize_multivalue(v, delim=','):
        # Accommodate messy input: translate everything to string and
        # tokenize by comma and/or whitespace delimiters (and strip
        # both kinds of delimiters from both ends of value string)
        v = str(v).strip(" \t,")
        return delim.join(re.split(r'[ \t,]+', v))

    for param, val in args.iteritems():

        # Ignore parameters specified with value=None
        if val == None:
            continue

        # Multiple values can be given as CSV (in a single string) or iterables
        if hasattr(val, '__iter__'):
            val = ",".join(map(str, val))
        else:
            val = str(val)
        if param in argspec.queryParams:
            if param == "format":
                clientParams["codec"] = val
                if val.lower() == CODEC_DJSON:
                    val = CODEC_JSON
            elif param == "page" and int(val) < 0:
                clientParams["pages"] = PAGES_ALL
                continue
            elif param_multivalued(param):
                val = normalize_multivalue(val)

            param = ParamAliases.get(param, param)
            restParams.append("%s=%s" % (param, val))
        elif param in argspec.pathParams:
            # Path params may be multivalued, too, so delimit them if so
            args[param] = normalize_multivalue(val, delim='%2C')
            continue
        else:
            raise TypeError("Unsupported method arg: %s" % param)

    restParams = "&".join(restParams)
    if restParams:
          restParams = "?" + restParams
    return restParams, clientParams

