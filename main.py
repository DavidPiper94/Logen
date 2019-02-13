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

##### common #####

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
    parser.add_argument("source", help = "Path to source directory")
    parser.add_argument("destination", help = "Path at which destination directory will be created")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--mock", action='store_true', help = "Präfixes all strings with the content of templates/template_common_mock. This can be used to check if all texts are localized.")
    group.add_argument("-l", "--long", action='store_true', help = "Präfixes all strings with the first 300 chars of 'Lorem ipsum' to test long strings.")
    return parser

def main(sourceFilenames, destinationDirectory, addMockText, addLongText):
    
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

if __name__ == "__main__":
    
    parser = setupParser()
    args = parser.parse_args()

    # get source dir and destination dir from given arguments
    sourceDirectory = args.source
    destinationDirectory = args.destination
    addMockText = args.mock
    addLongText = args.long
    
    # get all json files from source directory
    sourceFilenames = []
    for file in glob.glob("{}/*.json".format(sourceDirectory)):
        sourceFilenames.append(file)
    
    # start main function
    main(sourceFilenames, destinationDirectory, addMockText, addLongText)
