import os
import sys
import argparse
import subprocess   # for opening the generated directory
import glob         # for extracting all filenames from the given source directory
import shutil       # for deleting generated directory if it exists already

from lib import FileHelper
from lib import JsonHelper
from lib import TerminalStyle

import GeneratorIOS
import GeneratorIOSEnum
import GeneratorAndroid
import GeneratorJSON

def checkSourceFilepath(path):
    if not JsonHelper.isJSONFile(path):
        print(TerminalStyle.TerminalStyle.FAIL + "Given file is not a .json file. Converting cancled." + TerminalStyle.TerminalStyle.ENDC)
        sys.exit()
    else:
        return path

def createOrOverrideDirectory(path):
    if not os.path.exists(path):
        print("Creating directory {}".format(path))
        os.makedirs(path)
    else:
        print(TerminalStyle.TerminalStyle.WARNING + "Destination directory already existed. Overriding directory {}".format(path) + TerminalStyle.TerminalStyle.ENDC)
        shutil.rmtree(path)
        os.makedirs(path)

def openDirectory(directory):
    subprocess.check_call(['open', '--', directory])

def setupParser():
    parser = argparse.ArgumentParser(description = "Generates localization files for iOS and Android projects.")
    subparsers = parser.add_subparsers(title = "subcommands", 
                                       description = "Choose whether converting from a .json file to both an iOS and an Android localization or converting from a .strings iOS localization file or a .xml Android localization file to a common .json file.")

    mainParser = subparsers.add_parser("fromJSON", description = "Converts JSON files to both iOS and Android localiations.")
    mainParser.add_argument("source", help = "Path to source directory")
    mainParser.add_argument("destination", help = "Path at which destination directory will be created")
    group = mainParser.add_mutually_exclusive_group()
    group.add_argument("-m", "--mock", action='store_true', help = "Präfixes all strings with the content of templates/template_common_mock. This can be used to check if all texts are localized.")
    group.add_argument("-l", "--long", action='store_true', help = "Präfixes all strings with the first 300 chars of 'Lorem ipsum' to test long strings.")
    mainParser.set_defaults(func=generateCommonLocalization)

    subParser = subparsers.add_parser("toJSON", description = "Converts a given .strings iOS localization file or .xml Android localization file to a common JSON localization file.")
    subParser.add_argument("source", help = "Path to source file")
    subParser.add_argument("destination", help = "Path where created json file will be saved")    
    subParser.set_defaults(func=generateJSON)

    return parser

def generateCommonLocalization(args):
    
    # get source dir and destination dir from given arguments
    sourceDirectory = args.source
    destinationDirectory = args.destination
    addMockText = args.mock
    addLongText = args.long
    
    # get all json files from source directory
    sourceFilenames = []
    for file in glob.glob("{}/*.json".format(sourceDirectory)):
        sourceFilenames.append(file)

    # Construct destination paths.
    path = "{}/localization_gen".format(destinationDirectory)
    iosDestinationPath = "{}/ios".format(path)
    iosEnumDestinationPath = "{}/enum_swift".format(path)
    androidDestinationPath = "{}/android".format(path)
    
    # Create direcotries at destination paths.
    createOrOverrideDirectory(path)
    createOrOverrideDirectory(iosDestinationPath)
    createOrOverrideDirectory(iosEnumDestinationPath)
    createOrOverrideDirectory(androidDestinationPath)
    
    # Process each source file.
    for source in sourceFilenames:
        print(TerminalStyle.TerminalStyle.GREEN + "Converting file {}".format(path) + TerminalStyle.TerminalStyle.ENDC)
        filepath = checkSourceFilepath(source)
        dict = JsonHelper.readJSON(filepath)
        GeneratorIOS.writeIOSStringResource(dict, iosDestinationPath, addMockText, addLongText)
        GeneratorIOSEnum.writeIOSEnumFile(dict, iosEnumDestinationPath)
        GeneratorAndroid.writeAndroidStringResource(dict, androidDestinationPath, addMockText, addLongText)
            
    # Open the output directory.
    openDirectory(destinationDirectory)

def generateJSON(args):

    sourceFilepath = args.source
    destinationFilepath = args.destination
    
    extension = FileHelper.fileExtension(sourceFilepath)
    lines = FileHelper.readLines(sourceFilepath)

    if extension == ".strings":
        GeneratorJSON.convertIOSToJSON(lines, destinationFilepath)
    elif extension == ".xml":
        print("Converting of android localization currently not supported")
    else:
        print(TerminalStyle.TerminalStyle.FAIL + "Wrong file format." + TerminalStyle.TerminalStyle.ENDC)
        print("Please provide .strings file for existing iOS localization or .xml file for existing Android localization.")
        sys.exit()

if __name__ == "__main__":
    parser = setupParser()
    args = parser.parse_args()
    args.func(args)
