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

mockString = FileHelper.readFile("./templates/template_common_mock_string.txt")
longString = FileHelper.readFile("./templates/template_common_lorem.txt")

def showHelp():
    print("This pyhton script generates the localization for an iOS and an Android project.")
    print("It takes at least two arguments:")
    print("1) Path to source directory. This directory has to contain only json files.")
    print("2) Path to destination directory. Into this directory a new directory will be added which contains the generated files.")
    print("Additionally you can add following flags:")
    print("-h or --help: Shows this text as help.")
    print("-m or --mock: Präfixes all strings with {}. This can be used to check if all texts are localized.".format(mockString))
    print("-l or --long: Präfixes all strings with the first 300 chars of 'Lorem ipsum' to test long strings.")

def checkInput(arguments):
    
    if "-h" in sys.argv or "--help" in sys.argv:
        showHelp()
        sys.exit()
    
    if len(arguments) < 3:
        print(TerminalStyle.TerminalStyle.FAIL + "You provided not enough arguments." + TerminalStyle.TerminalStyle.ENDC)
        showHelp()
        sys.exit()
    
    if len(arguments) > 4:
        print(TerminalStyle.TerminalStyle.FAIL + "You provided too many arguments." + TerminalStyle.TerminalStyle.ENDC)
        showHelp()
        sys.exit()
    
    sourceDirectory = arguments[1]
    if not os.path.isdir(sourceDirectory):
        print(TerminalStyle.TerminalStyle.FAIL + "The source directory does not exist." + TerminalStyle.TerminalStyle.ENDC)
        showHelp()
        sys.exit()

def checkSourceFilepath(path):
    print(TerminalStyle.TerminalStyle.GREEN + "Converting file {}".format(path) + TerminalStyle.TerminalStyle.ENDC)
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

def main(sourceFilenames, destinationDirectory, mockText, longText):
    
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
        filepath = checkSourceFilepath(source)
        dict = JsonHelper.readJSON(filepath)
        GeneratorIOS.writeIOSStringResource(dict, iosDestinationPath, mockText, longText)
        GeneratorIOSEnum.writeIOSEnumFile(dict, iosEnumDestinationPath)
        GeneratorAndroid.writeAndroidStringResource(dict, androidDestinationPath, mockText, longText)
            
    # Open the output directory.
    openDirectory(destinationDirectory)

if __name__ == "__main__":
    checkInput(sys.argv)
    
    # get soruce dir and destination dir from given arguments
    sourceDirectory = sys.argv[1]
    destinationDirectory = sys.argv[2]
    mockText = "-m" in sys.argv or "--mock" in sys.argv
    longText = "-l" in sys.argv or "--long" in sys.argv
    
    # get all json files from source directory
    sourceFilenames = []
    for file in glob.glob("{}/*.json".format(sourceDirectory)):
        sourceFilenames.append(file)
    
    # start main function
    main(sourceFilenames, destinationDirectory, mockText, longText)
