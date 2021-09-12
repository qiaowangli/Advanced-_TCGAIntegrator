#!/usu/bin/end python
# encoding: utf-8

# Copyright (c) 2015-2017, Broad Institute, Inc. {{{
# All rights reserved.
#
# This file is part of fbgen, the automatic client bindings generator for the
# FireBrowse RESTful API (as wel as other well-formed, Swagger1-based APIs)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name Broad Institute, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
# }}}

from __future__ import print_function
import sys
import os
import time
import pprint
import textwrap
import stat
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pkg_resources import resource_filename
from fbimap import ParamAliases, fbHLMap
import fbcore as core
core.set_codec(core.CODEC_DJSON)
Output = core.dict2obj( { 'fp': sys.stdout, 'dirname': ''})
eprint   = core.eprint

FBMaps = "fbmap"
Ind4 = "    "
Ind8 = "        "
JSON2python = {
    'integer':'int',
    'string':'str',
    'number':'float',
    'boolean': 'bool'
}

def gopen(file, *args):
    ''' Ensure that generated files are always opened in '''
    if not file.startswith(Output.dirname):
        file = os.path.join(Output.dirname, file)
    return open(file, *args)

def insert_file(fname):
    for line in open( resource_filename(__name__, fname), "r"):
        emit(line.rstrip())

def copy_file(fname):
    from shutil import copy
    from_file_path = resource_filename(__name__, fname)
    copy(from_file_path, Output.dirname)

def get_client_version():
    version = open( resource_filename(__name__, "VERSION"), "r")
    return version.readlines()[0].rstrip()

def emit(s, *args):
    indent = Ind4 * args[0] if args else ''
    print( (indent + s).expandtabs(4), file=Output.fp)

def emit_docstr(s, *args):
    indent = '\t' * args[0] if args else '\t'
    emit('%s\'\'\'\n%s\n%s\'\'\'' % (indent, s, indent))

def params2argspec(parameters):
    # An argument specification object partitions the parameter list into
    # required/semi-required/path/query params, and also builds a docstr
    docs = ""
    spec = core.dict2obj({})
    spec.requiredParams = []
    spec.semiReqParams  = []
    spec.defaults       = []          # one per each semiReq-uired param
    spec.pathParams     = []
    spec.queryParams    = []

    for p in sorted(parameters, key=lambda elem:elem.paramType):
        docs += '\n\t\t\t%s  (%s' % (p.alias, JSON2python[p.type])
        if p.paramType == "path":
            spec.requiredParams.append(p.alias)
            spec.pathParams.append(p.alias)
        else:
            if p.optionality == "no":
                param = p.alias
                if p.defaultValue:
                    # Required parameters with default values are
                    # effectively optional/semiRequired parameters
                    spec.semiReqParams.append(param)
                    spec.defaults.append('\'%s\'' % p.defaultValue)
                else:
                    spec.requiredParams.append(param)
            elif p.optionality == "partial":
                spec.semiReqParams.append(p.alias)
                spec.defaults.append(None)
            spec.queryParams.append(p.alias)

        # Remove doc content that applies only to interactive UI
        description = p.description.replace(' from the scrollable list','')
        docs += ')  %s' % description

    spec.docs = docs
    return spec

def func_path2name(klass, func):

    # Skip class name +2 for leading and trailing slashes
    position = len(klass.name)+2
    name = func.path[position:].replace('/','')     # Remove all other / as wel

    # Strip out path parameters, which look like {parameterName}, if present
    position = name.find('{') + 1
    if position:
        param = name[position-1:]
        name = name[0:position-1]
        func.path = func.path.replace(param,'').rstrip('/')

    return name

def make_legal_python_name(name):
    # Use string.maketrans if this needs to do more than 1 character
    return name.replace('-','_')

def emit_function(klass, func):

    for endp in func.endpoints:
        if endp.notes:
            docs =  endp.notes
        else:
            docs =  endp.summary
        docs =  textwrap.fill(docs, initial_indent=Ind8, subsequent_indent=Ind8)
        docs += '\n\n\t\t'
        docs += 'For more details consult the interactive documentation at'
        docs += '\n\t\t'
        docs += '\t%s/#!/%s' % (core.get_uidocspath(), klass.name)
        docs += '\n\t\t'
        docs += 'OR use help(param_values) to see the range of values accepted'
        docs += '\n\t\t'
        docs += 'for each parameter, the defaults for each (if any), and the'
        docs += '\n\t\t'
        docs += 'degrees of optionality/requiredness offered by the API.'
        docs += '\n\n\t\t'
        docs += 'Parameters: '

        spec = endp.parameters
        docs += spec.docs
        del spec.docs                       # remove from spec: no longer needed

        requiredParams = list(spec.requiredParams)              # deep copy
        requiredParams.insert(0, 'self')
        requiredParams = ', '.join(requiredParams)
        emit ('@autohelp(%s)' % (len(spec.semiReqParams) > 0), 1)

        # Note that when more >1 endpoint is supported per func then func.name
        # alone cannot be used to name the wrapper function generated here
        # E.G. post/get/update endpoints should NOT all map to same name
        emit ('def %s(%s, **kwargs):' % (func.pyName, requiredParams), 1)

        emit_docstr(docs, 2)
        emit('')
        emit('vars = locals()', 2)
        specstr = pprint.pformat(vars(spec), indent=0)
        specstr = specstr.replace('\n','\n\t\t\t')
        specstr = specstr[:-1] + ",\n\t\t\t'caller' : self}"
        emit('spec = dict2obj(' + specstr + ')', 2)
        emit('queryParams, clientParams = parse_args(vars, spec)',2)

        emit('call = "%s%s"' % (klass.version, func.path), 2)
        if spec.pathParams:
            emit('call += "/%s" % "/".join([vars[p] for p in spec.pathParams])',2)

        emit('call += queryParams', 2)
        emit('return get(call, **clientParams)', 2)
        emit('')

def emit_klass(klass):
    emit('class %s (object):' % klass.name)
    emit("\t''' %s '''\n" % klass.description)
    emit('def __init__(self, format=CODEC_JSON, page=1, page_size=None):',1)
    emit('self.default_format = format', 2)
    emit('self.default_page  = page', 2)
    emit('self.default_page_size  = page_size if page_size else get_page_size()', 2)
    emit('')

    for func in klass.functions:
        emit_function(klass, func)

def emit_header():
    emit('')
    emit('# This file is part of %s: Python wrappers for the %s '\
         'RESTful api' % (Output.cliname, Output.dirname))
    emit('# Autogenerated on '+ time.strftime('%Y_%m_%d %X %Z'))
    emit('')
    emit('__version__ = \'%s\'' % get_client_version())

def emit_dict(theDict, itsName, exclude=[]):
    emit('')
    emit('%s = {   #  {{{' % itsName)
    for key, value in theDict.iteritems():
        if key in exclude:
            continue
        emit("'%s' : %s," % (key, pprint.pformat(value, indent=4)))
    emit('}  # }}}')

def emit_maps(api):
    # Emit data structures to support mapping types, names, parameters
    Output.fp = gopen(FBMaps + ".py", "w")
    emit_header()
    emit_dict(api.supported_params, "SupportedParameters")
    emit_dict(ParamAliases, 'ParamAliases')
    emit_dict(fbHLMap, 'fbHLMap')
    Output.fp.close()

def emit_lowlevel(api):

    Output.fp = gopen("lowlevel.py", "w")

    emit_header()
    insert_file("LICENSE.txt")
    emit(' ')
    emit('from %s import *' % FBMaps)
    emit('from fbcore import *')
    emit(' ')

    insert_file("parse.py")

    emit('')
    emit('def client_version():')
    emit('    return __version__')

    for klass in api.interface:
        emit_klass(klass)

    Output.fp.close()

    # Create __init__.py so import package transparently imports lowlevel funcs
    init_fp = gopen("__init__.py", "w")
    init_fp.write("from lowlevel import *\n")

    # Finally, copy in supportng code so that packages created by the generator
    # ALSO have access (NB: all code can in principle be emitted to just 1 file)
    copy_file("fbcore.py")
    copy_file("template.setup")

def lpaste(list1, list2, trimmer=None, combiner="%s=%s"):
    # Create a list of tuples, from the elements of each list
    result = zip(list1, list2)
    # Combine the tuple values
    result = map( lambda pair : combiner % pair, result)
    # Reduce elements in the result, if asked
    if trimmer:
        result = map(lambda x: x.replace(trimmer, ''), result)
    return result

def emit_high_level_functions(klass):

    portal = core.get_portalname()

    # First instantiate the object containing each function to be wrapped
    emit('')
    instance = "__" + klass.name
    emit('%s = %s(format=CODEC_TSV, page=PAGES_ALL)' % (instance, klass.name))

    # Now wrap each function
    for func in klass.functions:
        for endp in func.endpoints:

            # Map lowlevel funcs to "more Pythonic" (friendly) highlevel
            llname = "%s.%s" % ( klass.name, func.pyName)
            hlmap = fbHLMap.get(llname, {})
            if not hlmap:
                print("Warning: % not in highlevel map, is it new?" % func.name)
                continue

            # Build signature:  begin with mandatory/required params
            pars = endp.parameters
            reqParams = list(pars.requiredParams)         # deep copy

            # Now tack on the semiRequired params, with suitable defaults
            reqParams.extend( lpaste(pars.semiReqParams, pars.defaults) )

            # Now emit the function definition: first the name & signature...
            emit('')
            emit('@hlwrap("%s")' % llname)
            reqParams = ", ".join(reqParams)
            reqParams = reqParams + ", " if reqParams else ""
            emit('def %s(%s**kwargs):' % (hlmap['name'], reqParams))

            # ... and now the body
            docs  = '\t'
            docs += 'High level wrapper for the %s %s method.' % (portal,llname)
            docs += '\n\t'
            docs += 'By default it returns ALL pages of data, in TSV format.'
            emit_docstr(docs, 1)
            reqParams = pars.requiredParams
            reqParams.extend( [arg+"="+arg for arg in pars.semiReqParams] )
            reqParams = ",".join(reqParams)
            reqParams = reqParams + "," if reqParams else ""
            emit("return %s.%s(%s**kwargs)" % (instance, func.pyName, reqParams), 1)

def emit_highlevel(api):

    Output.fp = gopen("highlevel.py", "w")

    emit('#!/usr/bin/env python')
    emit_header()
    insert_file("LICENSE.txt")

    emit('')
    emit('import os')
    emit('import sys')
    emit('import argparse')
    emit('import __builtin__')

    emit('')
    emit('from %s import *' % core.get_portalname())
    emit('set_basepath("%s")' % api.basepath)

    emit('')
    emit('# Stop Python from complaining when I/O pipes are closed')
    emit('if os.name == \'posix\':')
    emit('    from signal import signal, SIGPIPE, SIG_DFL')
    emit('    signal(SIGPIPE, SIG_DFL)')

    for klass in api.interface:
        emit_high_level_functions(klass)

    # Be nice to users: expose help and param_* funcs at CLI, too
    emit('')
    for func in ['param_names', 'param_values', 'help', 'client_version']:
        emit('fbHLMap["%s"] = %s' % (func, func))

    insert_file("cli.py")
    Output.fp.close()

def emit_cli():
    toolname = Output.cliname
    Output.fp = open(toolname, "w")
    emit("#! /bin/bash")
    emit("# %s CLI wrapper to facilitate pre-installation testing" % toolname)
    emit("export PYTHONPATH=$PWD")
    emit('exec %s %s/highlevel.py "$@"' % (sys.executable, Output.dirname))
    # Ensure that execute permissions are set
    st = os.stat(toolname)
    new_mode = st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(Output.fp.name, new_mode)
    Output.fp.close()

def emit_setup(api):

    portal = Output.dirname
    generator = "'fbgen = firebrowse.generate:main'"
    pkgdata   = "package_data = {'':['VERSION','LICENSE.txt','template.setup']}"

    variables = {
    'PACKAGE'      : portal,
    'PORTAL'       : portal,
    'NOW'          : time.strftime('%Y_%m_%d__%H_%M_%S %Z', time.localtime()),
    'VERSION'      : get_client_version(),
    'URI'          : api.docs_uri,
    'CLINAME'      : Output.cliname,
    'YEAR'         : time.strftime('%Y', time.localtime()),
    'GENERATOR'    : generator if portal == 'firebrowse' else '',
    'PACKAGE_DATA' : pkgdata if portal == 'firebrowse' else '',
    }

    code = open(resource_filename(__name__, "template.setup"), "r").read()
    for var,value in variables.items():
        if value == None:
            value = "''"
        code = code.replace('%'+var+'%', value)
    open("setup.py", "w").write(code)

def generate(api):
    if not api.interface:
        return
    if not Output.dirname:
        Output.dirname = core.get_portalname()
    if not os.path.isdir(Output.dirname):
        os.makedirs(Output.dirname)

    #  This code generator creates 3 types of client interfaces:
    #
    #  Low level Python bindings:  which aim to map 1-1 with RESTful API
    #  High level Python bindings: which are more powerful and convenient than
    #                              the low-level bindings, by composing them
    #                              multiple low-level calls together to achieve
    #                              more with less code, and by setting defaults
    #                              automatically
    #  UNIX cli tool:              which wraps the high-level bindings into a
    #                              tool that is convenient to use at a UNIX
    #                              prompt; and therefore brings the entire UNIX
    #                              environment and suite of tools to bear for
    #                              use with FireBrowse

    emit_maps(api)
    emit_lowlevel(api)
    emit_highlevel(api)
    emit_cli()
    emit_setup(api)

def summarize(api):
    print("INTERFACE DEFINED BY: %s/" % api.basepath)
    for klass in api.interface:
        print("\n    API :\t%-36s%s" % (klass.path, klass.description))
        for func in klass.functions:
            for endp in func.endpoints:

                spec = endp.parameters

                # Convenience: explicitly list the 'path' parameters
                path = func.path
                for pathParam in spec.pathParams:
                    path += '/{%s}' % pathParam

                print("%48s%s%s" % (klass.version + path, Ind4, endp.summary))
                if spec.requiredParams:
                    emit("required: " + ", ".join(spec.requiredParams), 13)
                if spec.semiReqParams:
                    signat = lpaste(spec.semiReqParams, spec.defaults, "=None")
                    emit("semi-required: " + ", ".join(signat), 13)

class Api(object):
    def __init__(self, uri):
        if os.path.isfile(uri):
            self.load_raw_interface = self.load_from_file
            self.basepath = uri
        else:
            self.load_raw_interface = self.load_from_www
            if not uri.startswith('http'):
                uri = 'http://' + uri
            self.docs_uri = uri
            # Assume: basepath of API calls obtained by removing last path element
            sections = uri.rstrip('/').split('/')
            if core.get_verbosity():
                eprint("Setting basepath & uidocspath, contacting server ...")
            self.basepath = '/'.join(sections[0:-1])
            core.set_basepath(self.basepath)
            # Assumption: interactive UI docs are at <basepath>/../api-docs
            core.set_uidocspath('/'.join(sections[0:-2] + ['api-docs']))

        self.interface = []                         # initially empty
        self.supported_params = {}

    def load_from_www(self):
        if core.get_verbosity():
            eprint("Attempting to retrieve interface from "+self.docs_uri)
        try:
            # Turn toplevel groups of similar API funcs into equivalence klasses
            groups = core.get(self.docs_uri)['apis']            # returns a list
        except Exception, e:
            print("  Error accessing %s:\n\t%s" % (self.basepath, str(e)))
            groups = []

        klasses = []
        for klass in groups:
            klass = core.dict2obj(klass)
            path = self.basepath + klass.path

            try:
                if core.get_verbosity():
                    eprint("Retrieving method definition for "+path)
                functions = core.get(path)                      # returns a dict
            except Exception, e:
                print("  Error accessing method %s:\n\t%s" % (path, str(e)))
                functions = { 'apis' : [], 'apiVersion' : 'unknown' }

            # FIXME:  version should really be member of Api object, not klass
            #         b/c it should absolutely NOT be different for any klass
            #         (and in fact we can use Api.version to verify this & abort)
            klass.version = functions['apiVersion']
            klass.name = klass.path.replace('/%s/' % klass.version,'')
            klass.functions = functions
            klasses.append(klass)

        return klasses

    def define_interface(self):

        # Retrieve the API definition, or interface, and normalize its structure
        # and nomenclature for cleaner, more readable code & maintainability:
        #
        #   change dicts to objects to enable <obj>.<field> syntax, and prefer
        #   'version' over 'apiVersion'
        #   'endpoints' over 'operations'
        #   'functions' over (the duplicate use of) 'apis'
        #   'values' over 'enum' to express legal values of a parameter
        #
        # An interface is a list of klasses, each of which contain a list
        # of functions, each of which contain a list of endpoints
        #
        # fields in klass    obj: name,path,functions,version,description
        # fields in function obj: name,path,endpoints
        # fields in endpoint obj: parameters,type,notes,nickname,method,summary

        if self.interface:
            return

        self.interface = self.load_raw_interface()

        for klass in self.interface:

            def normalize(func):
                func['endpoints'] = func.pop('operations')
                func = core.dict2obj(func)
                func.endpoints = map(core.dict2obj, func.endpoints)
                func.name = func_path2name(klass, func)
                func.pyName = make_legal_python_name(func.name)
                def pnormalize(param):
                    param['values'] = param.pop('enum', [])
                    param = core.dict2obj(param)
                    param.alias = ParamAliases.get(param.name, param.name)
                    # If no list of permissible values has been defined for this
                    # parameter instance then default to its textual description
                    if not param.values:
                        param.values = [param.description]
                    param.defaultValue = getattr(param,'defaultValue', None)
                    # Store permissible values for easy lookup by users (via
                    # APIParameters), but do not overwrite existing values
                    if not self.supported_params.get(param.name, None):
                        self.supported_params[param.alias] = {
                                    'name': param.name,
                                    'alias': param.alias,
                                    'values': param.values,
                                    'multiValued': param.allowMultiple,
                                    'default' : param.defaultValue}
                    return param

                for endp in func.endpoints:
                    endp.parameters = map(pnormalize, endp.parameters)
                    endp.parameters = params2argspec(endp.parameters)

                # Store params in high level map for later lookup at runtime
                p = endp.parameters
                p = {"required" : p.requiredParams,
                     "semiReq"  : p.semiReqParams}
                fullname = klass.name + "." + func.pyName
                mapping = fbHLMap.get(fullname, None)
                if not mapping:
                    mapping = {'name' : func.pyName.lower()}
                    fbHLMap[fullname] = mapping
                    if core.get_verbosity():
                        eprint("Warning: made default highlevel mapping for %s;"\
                        "\n\t\tconsider adding to fbimap.py instead" % fullname)

                mapping["params"] = p
                return func
            
            klass.functions = map(normalize, klass.functions['apis'])

    def walk(self, walker=summarize):
        self.define_interface()
        walker(self)

def main(argv=None):
    
    description = "Encapsulate well-formed, SWAGGER1 RESTful API into Python "\
    "and UNIX client\nbindings, by retrieving its definition from a given URI\n"

    parser = ArgumentParser(description=description,
            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-c', '--cliname', default='fbget', help='name to '\
            'assign the tool which wraps the generated Python bindings in '\
            'a UNIX command line interface (default: %(default)s)')
    parser.add_argument('-m', '--map', default=None, help='not implemented '\
            'yet, but intended to supplement the internal mappings used by '\
            'the generator to assign high-level client function names that '\
            'are more easy/convenient to use than their RESTful counterparts')
    parser.add_argument('-o', '--outdir', default=None, dest='dirname',
            help='name of the output directory into which code will be '\
            'generated; this name is also assigned to the generated '\
            'Python package, and by default is inferred from the portal '\
            'name given in the URI offering the RESTful API definition')
    parser.add_argument('-s', '--summarize', default=False, action='store_true',
            help='Give concise summary of entire API, instead of "\
            generating wrappers? [%(default)s]')
    parser.add_argument('-u','--uri',
            default='http://firebrowse.org/api/api-docs/',
            help='Override default URI from which the API definition will '\
            'be retrieved [%(default)s].  This may be another WWW url or '\
            'a path to a local file containing the API definition.')
    parser.add_argument('-v', '--version', action='version',
            version='v%s' % get_client_version())
    parser.add_argument('-V', '--verbose', action='store_true',
            help='emit to stderr RESTful calls made, etc [False]')
 
    options = parser.parse_args()
    Output.dirname = options.dirname
    Output.cliname = options.cliname

    if options.summarize:
        walker = summarize
    else:
        walker = generate

    core.set_verbosity(options.verbose)

    Api(options.uri).walk(walker)

    return 0

if __name__ == '__main__':
    sys.exit(main())
