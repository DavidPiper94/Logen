import argparse
import sys

from localizer.converter.AndroidConverter import AndroidConverter
from localizer.converter.JSONConverter import JSONConverter
from localizer.converter.iOSConverter import iOSConverter

from localizer.lib import FileHelper
from localizer.lib import TerminalStyle

#--------------------
# Global vars
#--------------------

sourceFilepath = ""
destinationDirectory = ""
inputConverterIdentifier = ""
outputConverterIdentifier = ""
dryRun = False

def registeredConverter():
    return [
        iOSConverter(),
        AndroidConverter(),
        JSONConverter()
    ]

#--------------------
# Setup of main and subparsers
#--------------------

def setupParser():
    parser = argparse.ArgumentParser(description = "Description")
    subparsers = parser.add_subparsers(help = "Subparser")

    parser_convert = subparsers.add_parser("convert", help = "Lists all available converter.")
    parser_convert.add_argument("source", help = "Path to source file")
    parser_convert.add_argument("destination", help = "Path at which destination directory will be created")
    parser_convert.add_argument("inputConverter", help = "Identifier of the converter to be used to import content of the given file.")
    parser_convert.add_argument("outputConverter", help = "Identifier of the converter to be used to export content with a specific format.")
    parser_convert.add_argument("-d", "--dryRun", action = 'store_true', help = "If true, result will be printed to the console and not saved.")
    parser_convert.add_argument("-v", "--verbose", action = "store_true", help = "If true, additional information will be written to the console.")
    parser_convert.set_defaults(func = startConverting)

    parser_list = subparsers.add_parser("list", help = "Lists all available converter.")
    parser_list.set_defaults(func = listConverter)

    return parser

#--------------------
# Subcommand list
#--------------------

def listConverter(args):
    print(list(map(lambda x: describe(x), registeredConverter())))

def describe(converter):
    return converter.identifier()

#--------------------
# Subcommand convert
#--------------------

def startConverting(args):
    parseArgsForConverting(args)
    intermediate = importToIntermediateLocalization(sourceFilepath)
    exportToLocalizationFile(intermediate)

def parseArgsForConverting(args):

    # select and validate converter for output
    global outputConverterIdentifier
    outputConverterIdentifier = args.outputConverter
    selectedOutputConverter = list(filter(lambda x: x.identifier() == outputConverterIdentifier, registeredConverter()))
    if len(selectedOutputConverter) == 0:
        handleError("ERROR: Converter with identifier {} not found".format(outputConverterIdentifier))

    # validate source filepath
    global sourceFilepath
    sourceFilepath = args.source
    if not FileHelper.exists(sourceFilepath):
        handleError("ERROR: Source does not exists")
        
    # select and validate converter for input
    global inputConverterIdentifier
    inputConverterIdentifier = args.inputConverter
    extension = FileHelper.fileExtension(sourceFilepath)
    # TODO: Better comparison, e.g. lowercased
    matchingInputConverter = list(filter(lambda x: x.fileExtension() == extension and x.identifier() == inputConverterIdentifier, registeredConverter()))
    if len(matchingInputConverter) == 0:
        handleError("ERROR: No matching converter found with identiier {} for fileextension {}".format(inputConverterIdentifier, extension))
    else:
        inputConverterIdentifier = matchingInputConverter[0].identifier()
    
    # save and handle dryRun argument
    global dryRun
    dryRun = args.dryRun
    if dryRun:
        if args.verbose:
            printSummary(sourceFilepath, "dryRun", inputConverterIdentifier, outputConverterIdentifier)
        # If dryRun is enabled, there is no need to process destination directory.
        return

    # save and validate destination filepath
    global destinationDirectory
    destinationDirectory = args.destination
    if not FileHelper.exists(destinationDirectory):
        FileHelper.createDir(destinationDirectory)
    else:
        handleWarning("WARNING: Destination directory already exists. Do you want to override it?")
        # TODO: Ask
        #FileHelper.removeDir(destinationDirectory)
        #FileHelper.createDir(destinationDirectory)
    
    # At this point everything was validated and nothing can go wrong (hopefully).
    if args.verbose:
            printSummary(sourceFilepath, destinationDirectory, inputConverterIdentifier, outputConverterIdentifier)

def importToIntermediateLocalization(sourceFilepath):
    importer = list(filter(lambda x: x.identifier() == inputConverterIdentifier, registeredConverter()))
    return importer[0].toIntermediate(sourceFilepath)

def exportToLocalizationFile(intermediateLocalization):
    outputConverter = list(filter(lambda x: x.identifier() == outputConverterIdentifier, registeredConverter()))
    for output in outputConverter:
        for file in output.fromIntermediate(intermediateLocalization):
            handleLocalizationFile(file)

def handleLocalizationFile(localizationFile):
    global dryRun
    if dryRun:
        print(localizationFile.filecontent)
    else:
        destination = destinationDirectory + "/" + localizationFile.filepath
        writeFile(destination, localizationFile.filecontent)

def writeFile(path, content):
    directoryPath = FileHelper.directoryPath(path)

    if FileHelper.exists(path):
        pass

    else:
        FileHelper.createDir(directoryPath)
        FileHelper.writeFile(path, content)

#--------------------
# cli output
#--------------------

def printSummary(sourceFilepath, destinationFilepath, inputConverterIdentifier, outputConverterIdentifier):
    handleInfo(
        "Summary:\n"
        + "input: {}\n".format(sourceFilepath)
        + "output: {}\n".format(destinationFilepath)
        + "converter for input: {}\n".format(inputConverterIdentifier)
        + "converter for output: {}".format(outputConverterIdentifier)
    )

def handleError(errorText):
    print(TerminalStyle.FAIL + errorText + TerminalStyle.ENDC)
    sys.exit()

def handleWarning(warningText):
    print(TerminalStyle.WARNING + warningText + TerminalStyle.ENDC)

def handleInfo(infoText):
    print(TerminalStyle.GREEN + infoText + TerminalStyle.ENDC)

#--------------------
# Main
#--------------------

if __name__ == '__main__':
    parser = setupParser()
    args = parser.parse_args()
    args.func(args)
    
