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

#--------------------
# Parsing of arguments
#--------------------

def handleArguments():
    parser = setupParser()
    parseArguments(parser)

def setupParser():
    parser = argparse.ArgumentParser(description = "Description")
    parser.add_argument("source", help = "Path to source file")
    parser.add_argument("destination", help = "Path at which destination directory will be created")
    parser.add_argument("converter", help = "Identifier of the converter to be used")
    parser.add_argument("-d", "--dryRun", action = 'store_true', help = "If true, result will be printed to the console and not saved.")
    return parser

def parseArguments(parser):
    args = parser.parse_args()

    # select and validate converter for output
    global outputConverterIdentifier
    outputConverterIdentifier = args.converter
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
    extension = FileHelper.fileExtension(sourceFilepath)
    # TODO: Better comparison, e.g. lowercased
    matchingInputConverter = list(filter(lambda x: x.fileExtension() == extension, registeredConverter()))
    if len(matchingInputConverter) == 0:
        handleError("ERROR: No matching converter found for fileextension {}".format(extension))
    else:
        inputConverterIdentifier = matchingInputConverter[0].identifier()
    
    # save and handle dryRun argument
    global dryRun
    dryRun = args.dryRun
    if dryRun:
        # If dryRun is enabled, there is no need to process destination directory.
        return

    # save and validate destination filepath
    global destinationDirectory
    destinationDirectory = args.destination
    if not FileHelper.exists(destinationDirectory):
        FileHelper.createDir(destinationDirectory)
    else:
        print("WARNING: Destination directory already exists. Do you want to override it?")
        # TODO: Ask
        #FileHelper.removeDir(destinationDirectory)
        #FileHelper.createDir(destinationDirectory)

def handleError(errorText):
    print(TerminalStyle.FAIL + errorText + TerminalStyle.ENDC)
    sys.exit()

#--------------------
# Converting
#--------------------

def registeredConverter():
    return [
        iOSConverter(),
        AndroidConverter(),
        JSONConverter()
    ]

def importToIntermediateLocalization(sourceFilepath):
    importer = list(filter(lambda x: x.identifier() == inputConverterIdentifier, registeredConverter()))
    return importer[0].toIntermediate(sourceFilepath)

def exportToLocalizationFile(intermediateLocalization):
    outputConverter = list(filter(lambda x: x.identifier() == outputConverterIdentifier, registeredConverter()))
    for output in outputConverter:
        for file in output.fromIntermediate(intermediate):
            handleLocalizationFile(file)

#--------------------
# Output
#--------------------

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
# Main
#--------------------

if __name__ == '__main__':
    handleArguments()
    intermediate = importToIntermediateLocalization(sourceFilepath)
    exportToLocalizationFile(intermediate)
    
