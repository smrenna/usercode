#!/usr/bin/env python


## TODO : accept input as part of input file instead of always command line


import distutils
import distutils.fancy_getopt
import os
import sys
import string
import re
import commands
import random
import stat
import glob


#---Settings----#000000#FFFFFF--------------------------------------------------

class Color:
  "ANSI escape display sequences"
  info        = "\033[1;34m"
  hilight     = "\033[31m"
  alternate   = "\033[32m"
  backlight   = "\033[43m"
  underline   = "\033[4m"
  deemphasis  = "\033[1;30m"
  none        = "\033[0m"

class Error:
  "Exit codes"
  none        = 0
  usage       = 1
  argument    = 2
  execution   = 3
  data        = 4

class Settings:
  "Settings for execution etc."

  blurb         = """
Usage: %prog [options] <template-files...> [parameter-values/conditions] ...

The optional arguments (after the sms-template file) can be made up of any
number of parameter value specifications:
  parameter = value1, value2, ...
whereby the parameter will be substituted with the various values in different
generated configurations. A range from start to end (inclusive) can be specified using
  parameter = start-end:step
You can also specify conditions, e.g.
  parameter1 < parameter2
or any other Python-understandable command. The regions of parameter space that
are scanned will be made to satisfy all stated conditions.

Of course, you may need to quote the parameter-values/conditions so that your shell
doesn't break them up into itsy bitsy pieces. For example:

  %prog my_sms.template Mbigthing=500-1000:200 Msmallthing=50,600 'Mbigthing > Msmallthing'
  
Extended syntax:
Sets of substitution rules can be specified by enclosing the desired ranges within square
brackets, e.g.
  %prog my_sms.template [Mbig=500-800:200 Msmall=50,100 alpha=0.2] \
                        [Mbig=800-1000:200 Msmall=150,200,300 alpha=1.3]
Specifications outside of square brackets will be repeated for all of the substitution sets.


Command-line options can be:
"""
  variables       = distutils.fancy_getopt.FancyGetopt([
                      ("help",                    "h",  "Print this informational message."),
                      ("dry-run",                 "d",  "Prints out commands, but doesn't execute them or make any files."),
                      ("job-directory=",          "i",  "Location to create jobs in. Default '%job-directory%'."),
                      ("data-directory=",         "D",  "Location to create data files in, i.e. those to be passed to cmsRun jobs. Assumed to be relative to cmssw-project-path/src. Default '%data-directory%'."),
                      ("data-file-mask=",         "f",  "Semi-colon separated list of glob expressions to match template instances that have to be moved to data-directory. Default '%data-file-mask%'."),
                      ("sms-template=",           "t",  "Extension of template files from which to extract the sms name. Default '%sms-template%'."),
                      ("cmssw-project-path=",     "C",  "Directory containing the CMSSW project to use. Default '%cmssw-project-path%'."),
                      ("sms-name-tag=",           None, "Tag to substitute with the sms name (from the template name, no extension). Default '%sms-name-tag%'."),
                      ("sms-label-tag=",          None, "Tag to substitute with the sms label (from the template name, no extension). Default '%sms-label-tag%'."),
                      ("sms-xsec-tag=",           None, "Tag to substitute with the sms cross-section, as specified via the cross-section parameter. Default '%sms-xsec-tag%'."),
                      ("sms-params-tag=",         None, "Tag to substitute with the modules to store SMS model parameters. Default '%sms-parameters-tag%'."),
                      ("job-dir-tag=",            None, "Tag to substitute with job-directory. Default '%job-dir-tag%'."),
                      ("data-dir-tag=",           None, "Tag to substitute with data-directory. Default '%data-dir-tag%'."),
                      ("cross-section=",          "x",  "'path:histogram' string specifying the ROOT file containing cross-section info and the histogram out of this file to use. If the histogram name does not correspond to the particle name, use the format 'path:histogram:particle-mass'. Default '%cross-section%'."),
                      ("env-template=",           None, "Regular expression for getting environment variables to put in templates. Must capture both the entire expression, and the variable name. Default '%env-template%'."),
                    ])
  options         = { "help"                  : False,
                      "dry-run"               : False,
                      "job-directory"         : "jobs",
                      "data-directory"        : "UserCode/SMSGeneration/data/__SMS_NAME__",
                      "data-file-mask"        : "*.slha",
                      "sms-template"          : "slha",
                      "cmssw-project-path"    : os.environ["CMSSW_BASE"],
                      "sms-name-tag"          : "__SMS_NAME__",
                      "sms-label-tag"         : "__SMS_LABEL__",
                      "sms-xsec-tag"          : "__SMS_CROSS_SECTION__",
                      "sms-params-tag"        : "__SMS_PARAMETERS__",
                      "job-dir-tag"           : "__JOB_PATH__",
                      "data-dir-tag"          : "__DATA_PATH__",
                      "cross-section"         : None,
                      "env-template"          : "(__ENV\(([^\)]+)\)__)",
                    }
  usage           = None

  scriptDir       = ""
  getParamValues  = re.compile("^([^=]+)\s*=\s*([^=]+)$")
  getValueRange   = re.compile("([^-]+)-([^:]+):(.+)")
  getFieldSetting = "^\s*%s\s*=\s*(.+)"
  sanitize        = re.compile("\s+")



#---Functions---#000000#FFFFFF--------------------------------------------------

def convertSetting(setting, convertor, errorMessage):
  """
  Convert the given setting using the form produced by convertor. ValueError's
  are caught and errorMessage is printed, then the application exits. errorMessage
  is a format string taking one string argument, the problematic value.
  """

  try:
    Settings.options[setting] = convertor(Settings.options[setting])
  except ValueError:
    print Color.hilight + (errorMessage % str(Settings.options[setting])) + Color.none
    sys.exit(Error.argument)

  return

def toNumber(streeng):
  try:
    return int(streeng)
  except ValueError:
    pass
  return float(streeng)

def toList(streeng, delimiter = ";"):
  streeng = streeng.strip()
  if streeng == "":   return []
  return string.split(streeng, delimiter)

def parseArgs(args):
  "Parses command-line arguments into options and variables"

  Settings.scriptDir  = os.path.dirname(os.path.abspath(args[0]))
  Settings.blurb      = Settings.blurb.replace("%prog", os.path.basename(args[0]))
  Settings.usage      = string.join(Settings.variables.generate_help(Settings.blurb), "\n")
  for (variable, default) in Settings.options.iteritems():
    if type(default) == type(""):
      Settings.options[variable]  = default.replace("%script-dir%", Settings.scriptDir)
  for (variable, default) in Settings.options.iteritems():
    Settings.usage    = re.compile("%" + variable.replace("-", "-\s*") + "%") \
                          .sub(str(default), Settings.usage)

  try:
    (arguments, options)  = Settings.variables.getopt(args[1:])
  except distutils.errors.DistutilsArgError, details:
    print "Error in command-line:", details
    print Settings.usage
    sys.exit(Error.usage)

  # Get the dictionary of option -> value
  Settings.options.update(dict(Settings.variables.get_option_order()))

  # Special options
  convertSetting("env-template"   , re.compile, "%s must be a valid regular expression.")
  convertSetting("data-file-mask" , toList    , "%s must be a semi-colon separated list.")
  Settings.getSMSInput  = re.compile("^([^.]+)[.]"+Settings.options["sms-template"])

  if Settings.options["help"] or len(arguments) < 2:
    print Settings.usage
    print
    sys.exit(Error.none)

  return arguments


def parseSpecifications(arguments):
  """
  Converts specifications of the format x=y,z,... into (parameter, values) and
  collects all others in the set of conditions. Output is
  ( [(param1, values1), (param2, values2), ...] , [condition1, condition2, ...] )
  """

  dataset           = None
  templates         = []
  summaries         = []
  parameterSets     = []
  commonSpecs       = []
  specifications    = []
  
  #-- Parse into parameter sets -----------------------------------------------
  isInCommon        = True
  for argument in arguments:
    argument        = argument.strip()
    if os.path.isfile(argument):
      matchDataset  = Settings.getSMSInput.search(os.path.basename(argument))
      if matchDataset:
        dataset     = matchDataset.group(1)
      templates.append(argument)
      continue
    
    if isInCommon:
      if argument.startswith("["):
        isInCommon  = False
        specifications.append([])
        argument    = argument[1:].strip()
    elif argument.endswith("]"):
      isInCommon    = True
      argument      = argument[:-1]
      if len(argument) > 0:
        specifications[-1].append(argument)
      continue
    
    if len(argument) < 1: continue
    if isInCommon:  commonSpecs.append(argument)
    else:           specifications[-1].append(argument)
  
  
  #-- Process each parameter set ----------------------------------------------
  for specification in specifications:
    specification   .extend(commonSpecs)
    paramValues     = []
    conditions      = []
    for spec in specification:
      result        = Settings.getParamValues.findall(spec)
      if result and len(result) == 1:
        values      = []
        for item in result[0][1].split(","):
          rangeSpec = Settings.getValueRange.match(item)
          if rangeSpec:
            start   = toNumber(rangeSpec.group(1))
            stop    = toNumber(rangeSpec.group(2))
            step    = toNumber(rangeSpec.group(3))
            while start <= stop:
              values.append(str(start))
              start = start + step
          else:
            values  .append(item)
        paramValues .append((result[0][0], values))
      else:
        conditions  .append(spec)

    parameterSets.append((paramValues, conditions))
    summary         = ""
    for (parameter, values) in paramValues:
      summary       = summary + parameter + "=" + string.join(values, ",") + "  "
    if len(conditions):
      summary       = summary + "where " + string.join(conditions, " and ")
    summaries.append(summary)

  return (dataset, templates, summaries, parameterSets)


def listSpecifications(parameterSets):
  """
  Parses specifications using parseSpecifications, then generates, using that
  information, all sets of parameter specifications allowed by the ranges and
  conditions. Returns
  [ [(p1,v11), (p2,v12), ...], [(p1,v21), (p2,v22), ...], ... ]
  """

  specifications            = []
  for (paramValues, conditions) in parameterSets:
    parameters              = []
    composition             = ""
    for (parameter, values) in paramValues:
      parameters            .append(  "('" + parameter + "'," + parameter + ")" )
      composition           = composition + " for " + parameter \
                            + " in [" + string.join(values, ",") + "]"
  
    comprehension           = "[ [" + string.join(parameters, ",") + "]" +  composition
    if len(conditions) > 0:
      comprehension         = comprehension + " if (" + string.join(conditions, " and ") + ")"
    comprehension           = comprehension + " ]"
    specifications.extend(eval(comprehension))

  return specifications



def runJob(commandLine, logPath = None, scriptFile = None, maybeRun = True):
  """
  Runs the specified command, saving the output and checking the status.
  """

  if maybeRun:
    if Settings.options["into-shell-script"] != None and scriptFile != None:
      print "     ", commandLine
      scriptFile.write(commandLine)
      scriptFile.write("\n")
      return ""
    if Settings.options["dry-run"] or Settings.options["dont-run"]:
      print "     ", commandLine
      return ""

  (status, output)  = commands.getstatusoutput(commandLine);
  if logPath:
    logFile = open(logPath, "w")
    logFile.write(output)
    logFile.close()

  if status != 0:
    print Color.hilight + "###", Color.none
    print Color.hilight + "###  PROBLEM    :", Color.none, commandLine.split(" ",1)[0], "exited with error code", status
    print Color.hilight + "###  Command    :", Color.none, commandLine
    print Color.hilight + "###  Output was :", Color.none
    print Color.hilight + "###", Color.none
    print output
    sys.exit(Error.execution)

  print Color.info, "    ", commandLine, Color.none
  if logPath:   print Color.alternate, "       ... successful" + Color.deemphasis + ", logged in", logPath, Color.none
  else:         print output
  return output


def readFile(fileName):
  if not os.path.isfile(fileName):
    print "ERROR : Could not access '" + fileName + "' for reading."
    sys.exit(Error.data)

  input = open(fileName, "r")
  data  = input.read()
  input.close()
  return data

def writeFile(fileName, data, verbose=False):
  if os.path.isfile(fileName):
    print Color.hilight + "WARNING", Color.none, " : '" + fileName + "' already exists, will be backed up to '" + fileName + ".bak'!"
    if os.path.isfile(fileName + ".bak"):
      os.remove(fileName + ".bak")
    os.rename(fileName, fileName + ".bak")

  if verbose:
    if Settings.options["dry-run"]:
      print Color.deemphasis + "+-> ", Color.none, fileName
      return
    print Color.deemphasis + "+->  ", fileName, Color.none

  output  = open(fileName, "w")
  output.write(data)
  output.close()
  return

def makeReplacements(string, replacements):
  for (pattern, replacement) in replacements:
    if type(pattern) == type(""):
      string  = string.replace(pattern, replacement)
    else:
      string  = pattern.sub(replacement, string)
  for (expression, variable) in Settings.options["env-template"].findall(string):
    string    = string.replace(expression, os.environ[variable])
  return string

def sortByValue(parameterSets):
  order           = parameterSets[0]
  order.sort(key = (lambda x: x[1]), reverse = True)
  sortedSets      = []
  for paramValues in parameterSets:
    paramValues   = dict(paramValues)
    if len(paramValues) != len(order):
      print Color.hilight + "ERROR: Inconsistent number of parameters.", Color.none
      sys.exit(Error.argument)
    sorted        = []
    for (parameter, value) in order:
      if parameter not in paramValues:
        print Color.hilight + "ERROR: Inconsistent list of parameters.", Color.none
        sys.exit(Error.argument)
      sorted.append((parameter, paramValues[parameter]))
    sortedSets.append(sorted)
  return sortedSets


#---Main Execution Point---#D50000#FFFF80---------------------------------------

if __name__ == '__main__':

  # Deduce set of parameters for scanning
  arguments         = parseArgs(sys.argv)
  (dataset, templatePaths, summaries, parameterSets) = parseSpecifications(arguments)
  print Color.info + "Specifications         :", Color.none,
  print string.join(summaries, "\n                          ")
  specifications    = listSpecifications(parameterSets)
  if len(specifications) < 1:
    print Color.hilight + "ERROR: No parameter values specified.", Color.none
    sys.exit(Error.argument)
  specifications    = sortByValue(specifications)

  # Input cross-sections
  xsecLookup        = None
  producedMass      = None
  if Settings.options["cross-section"]:
    sys.argv.append("-b")
    from ROOT import TH1, TFile
    (path,particle) = Settings.options["cross-section"].split(":",2)
    if ":" in particle:
      (particle,producedMass) = particle.split(":",2)
    else:
      for (parameter, value) in specifications[0]:
        if parameter[1:] == particle:
          producedMass= parameter
          break
    if not producedMass:
      print Color.hilight + "ERROR: Particle '" + particle + "' is not one of the list of mass parameters of this model.", Color.none
      sys.exit(Error.argument)
    
    xsecFile        = TFile.Open(path, "READ")
    if xsecFile.IsZombie():
      print Color.hilight + "ERROR: Failed to open cross-section file '" + path + "'.", Color.none
      sys.exit(Error.argument)
    xsecLookup      = xsecFile.FindObjectAny(particle)
    if xsecLookup == None or not xsecLookup.InheritsFrom("TH1"):
      print Color.hilight + "ERROR: Failed to load '" + particle + "' from '" + path + "'.", Color.none
      sys.exit(Error.argument)
  
    print Color.info + "Cross-section          :", Color.none, producedMass

  # Load templates
  print Color.info + "Job template(s)        :", Color.none, string.join(templatePaths, "\n" + (" "*26))
  jobTemplates      = map(readFile, templatePaths)

  # Setup paths
  runDir            = os.path.join(Settings.options["job-directory"], dataset)
  print Color.info + "Job directory          :", Color.none, runDir
  if not Settings.options["dry-run"] and not os.path.isdir(runDir):
    os.makedirs(runDir)

  print


  ###############
  # Create jobs #
  ###############

  previous          = None
  for specification in specifications:

    #---------------------------------------------------------------------------
    # Setup for this set of parameters
    #---------------------------------------------------------------------------
    smsLabel        = ""
    modelParams     = []
    paramWriters    = []
    paramModules    = []
    nextRow         = (previous == None)
    crossSection    = -9
    for index in range(len(specification)):
      (parameter, value)  = specification[index]
      if not nextRow and index < len(specification) - 1 and value != previous[index][1]:
        nextRow     = True
      
      writer        = "process.sms%s" % parameter
      paramWriters.append(writer)
      paramModules.append('''%s = cms.EDProducer("DoubleProducer", value = cms.double(%g))''' % (writer, value))
      if parameter == producedMass:
        crossSection= xsecLookup.GetBinContent(xsecLookup.GetXaxis().FindFixBin(value+1))

      value         = str(value)
      smsLabel      = smsLabel + "_" + parameter + "_" + value.replace(".", "-")
      modelParams.append((re.compile(r"\b"+parameter+r"\b"), value))
      
    smsLabel        = smsLabel.lstrip("_")
    modelParams.append((Settings.options["sms-name-tag"  ], dataset))
    modelParams.append((Settings.options["sms-label-tag" ], smsLabel))
    modelParams.append((Settings.options["sms-xsec-tag"  ], str(crossSection)))
    modelParams.append((Settings.options["sms-params-tag"], string.join(paramModules,"\n") + "\nprocess.storeSMSParameters = cms.Sequence(%s)" % string.join(paramWriters," * ")))
    modelParams.append((Settings.options["job-dir-tag"   ], os.path.abspath(runDir)))
    dataDir         = makeReplacements(Settings.options["data-directory"], modelParams)
    modelParams.append((Settings.options["data-dir-tag"  ], dataDir))
    dataDir         = os.path.join(Settings.options["cmssw-project-path"], "src", dataDir)
    if not os.path.isdir(dataDir):    os.makedirs(dataDir)
    previous        = specification
    
    if nextRow:
      print
      if xsecLookup:
        print " %10.6g pb : " % crossSection,
      print string.join(["%10s = %-5s" % spec for spec in specification[:-1]], ", ") + (", %10s = " % specification[-1][0]),
    print "%5s" % specification[-1][1],

    if Settings.options["dry-run"]: continue

    #---------------------------------------------------------------------------

    # Write concrete instances of all templates
    for (templateFile, template) in zip(templatePaths, jobTemplates):
      templateFile  = os.path.splitext(os.path.basename(templateFile))[0]
      (name, ext)   = os.path.splitext(templateFile)
      if name != dataset:
        name       += "_" + dataset
      name         += "_" + smsLabel
      targetName    = name+ext
      targetDir     = runDir
      for pattern in Settings.options["data-file-mask"]:
        if glob.fnmatch.fnmatch(targetName, pattern):
          targetDir = dataDir
          break
      
      writeFile(os.path.join(targetDir, name+ext), makeReplacements(template, modelParams))

