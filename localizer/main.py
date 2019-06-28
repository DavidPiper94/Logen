import argparse
import os

from localizer.converter.AndroidConverter import AndroidConverter
from localizer.converter.JSONConverter import JSONConverter
from localizer.converter.iOSConverter import iOSConverter

from localizer.lib import FileHelper

def setupParser():
    parser = argparse.ArgumentParser(description = "Description")
    parser.add_argument("source", help = "Path to source directory")
    parser.add_argument("destination", help = "Path at which destination directory will be created")
    parser.add_argument("-d", "--dryRun", action = 'store_true', help = "If true, result will be printed to the console and not saved.")
    return parser

def parseArguments(parser):
    args = parser.parse_args()
    print(args.dryRun)

def registeredConverter():
    return [
        iOSConverter(),
        AndroidConverter(),
        JSONConverter()
    ]

def selectImporterForFileExtension(extension):
    # TODO: Better comparison, e.g. lowercased
    return filter(lambda x: x.fileExtension() == extension, registeredConverter())[0]

def outputConverterForFileExtension(extension):
    # TODO: Better comparison, e.g. lowercased
    return filter(lambda x: x.fileExtension() != extension, registeredConverter())

def handleLocalizationFile(localizationFile, dryRun):
    if dryRun:
        print(localizationFile.filecontent)
    else:
        destination = "/Users/davidpiper/Desktop/rest/test/{}".format(localizationFile.filepath)#localizationFile.filepath
        FileHelper.writeFile(destination, localizationFile.filecontent)

if __name__ == '__main__':
    parser = setupParser()
    parseArguments(parser)

    # TODO: Check if path exists.
    path = "/Users/davidpiper/Developer/Projekte/Localizer/localizer/tests/testdata/ExampleJSON.json"
    extension = os.path.splitext(path)[-1].lower()
        
    importer = selectImporterForFileExtension(extension)
    if importer == None:
        # TODO: Better error message
        print("No converter found!")

    outputConverter = outputConverterForFileExtension(extension)

    intermediate = importer.toIntermediate(path)

    for output in outputConverter:
        for file in output.fromIntermediate(intermediate):
            handleLocalizationFile(file, setupParser().parse_args().dryRun)
    
