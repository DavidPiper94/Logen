import argparse

from localizer.converter.AndroidConverter import AndroidConverter
from localizer.converter.JSONConverter import JSONConverter
from localizer.converter.iOSConverter import iOSConverter

from localizer.lib import FileHelper

#--------------------
# Global vars
#--------------------

sourceFilepath = ""
destinationDirectory = ""
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
    parser.add_argument("-d", "--dryRun", action = 'store_true', help = "If true, result will be printed to the console and not saved.")
    return parser

def parseArguments(parser):
    args = parser.parse_args()

    global sourceFilepath
    sourceFilepath = args.source
    if not FileHelper.exists(sourceFilepath):
        print("ERROR: Source does not exists")
    
    global dryRun
    dryRun = args.dryRun

    # If dryRun is enabled, there is no need to process destination directory.
    if dryRun:
        return

    global destinationDirectory
    destinationDirectory = args.destination
    if not FileHelper.exists(destinationDirectory):
        FileHelper.createDir(destinationDirectory)
    else:
        print("WARNING: Destination directory already exists. Do you want to override it?")
        # TODO: Ask
        #FileHelper.removeDir(destinationDirectory)
        #FileHelper.createDir(destinationDirectory)

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
    extension = FileHelper.fileExtension(sourceFilepath)
    importer = selectImporterForFileExtension(extension)
    if importer == None:
        # TODO: Better error message
        print("No converter found!")
    else:
        return importer.toIntermediate(sourceFilepath)

def selectImporterForFileExtension(extension):
    # TODO: Better comparison, e.g. lowercased
    return list(filter(lambda x: x.fileExtension() == extension, registeredConverter()))[0]

def exportToLocalizationFile(intermediateLocalization):
    extension = FileHelper.fileExtension(sourceFilepath)
    outputConverter = outputConverterForFileExtension(extension)
    for output in outputConverter:
        for file in output.fromIntermediate(intermediate):
            handleLocalizationFile(file, setupParser().parse_args().dryRun)

def outputConverterForFileExtension(extension):
    # TODO: Better comparison, e.g. lowercased
    return list(filter(lambda x: x.fileExtension() != extension, registeredConverter()))

#--------------------
# Output
#--------------------

def handleLocalizationFile(localizationFile, dryRun):
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
    
