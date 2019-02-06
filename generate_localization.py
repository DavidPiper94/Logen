import os
import sys
import argparse
import subprocess   # for opening the generated directory
import glob         # for extracting all filenames from the given source directory
import shutil       # for deleting generated directory if it exists already

from lib import FileHelper
from lib import JsonHelper
from lib import TerminalStyle

##### common #####

mockString = "AAAAA"
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
    
    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(path)[-1].lower()
    if ext != ".json":
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

def makeCommonGeneratedWarning():
    return FileHelper.readFile("./templates/template_common_generated_warning.txt")

##### iOS Resource #####

def makeIOSGeneratedWarning():
    commonWarning = makeCommonGeneratedWarning()
    return "/*\n{}\n */\n".format(commonWarning)

def makeIOSEntry(key, value):
    value = value.replace("\"", "\\\"")
    value = value.replace("'", "\\'")
    return "\"{}\" = \"{}\";\n".format(key, value)

def writeIOSStringResource(dict, destinationDirectory, mockText, longText):
    print(type(dict))
    for sectionKey, sectionValue in dict.items():
        
        for languageKey, localization in sectionValue.items():
            
            # Create filename.
            filepath = "{}/{}.lproj".format(destinationDirectory, languageKey)
            filename = "{}/{}.strings".format(filepath, sectionKey)
            print("Writing file {}".format(filename))
        
            if not os.path.exists(filepath):
                print("Creating directory {}".format(filepath))
                os.makedirs(filepath)
        
            content = makeIOSGeneratedWarning()
            content += FileHelper.readFile("./templates/template_ios_section_header.txt").format(sectionKey)
            
            for key, value in localization.items():
                if mockText:
                    content += makeIOSEntry(key, "{} - {}".format(mockString,value))
                elif longText:
                    content += makeIOSEntry(key, "{} - {}".format(longString,value))
                else:
                    content += makeIOSEntry(key, value)
            # Save file.
            FileHelper.writeFile(filename, content)

##### iOS Enum #####

def makeIOSEnumEntry(key):
    newKey = key.replace(".", "_")
    return "        case {} = \"{}\"\n".format(newKey, key)

def writeIOSEnumFile(dict, destinationDirectory):

    for sectionKey, sectionValue in dict.items():
        
        # Create filename.
        # This line capitalizes the first letter in the sectionKey.
        # This is used as part of the filename, so it will be capitalizesd as it should be.
        # We can't use .capitalize() or .title() because that would lowercase all other chars.
        sectionName = ' '.join(word[0].upper() + word[1:] for word in sectionKey.split())
        filename = "{}/{}LocalizableKeys.swift".format(destinationDirectory, sectionName)
        print("Writing {}/{}Keys.swift".format(destinationDirectory, sectionName))
        
        for languageKey, localization in sectionValue.items():
            
            content = makeIOSGeneratedWarning()
            content += "\n// The MaternaAppKit-Framework is needed to extend the base class.\nimport MaternaAppKit\n\n"
            content += FileHelper.readFile("./templates/template_ios_enum_documentation.txt")
            content += "extension LocalizableKeys {\n"
            content += "    enum {0}: String {{\n".format(sectionKey)
            for key, value in localization.items():
                content += makeIOSEnumEntry(key)
            content += "    }\n"
            content += "}"

    FileHelper.writeFile(filename, content)

##### Android Resource #####

def makeAndroidGeneratedWarning():
    commonWarning = makeCommonGeneratedWarning()
    return "<!-- \n{} \n-->\n\n".format(commonWarning)

def makeAndroidEntry(key, value):
    value = value.replace("\"", "\\\"")
    value = value.replace("'", "\\'")
    return "    <string name=\"{}\">{}</string>\n".format(key, value)

def writeAndroidStringResource(dict, destinationDirectory, mockText, longText):
    
    for sectionKey, sectionValue in dict.items():
        
        for languageKey, localization in sectionValue.items():
            
            # Create filename.
            filepath = "{}/values-{}".format(destinationDirectory, languageKey)
            filename = "{}/{}.xml".format(filepath, sectionKey)
            print("Writing file {}".format(filename))
            
            if not os.path.exists(filepath):
                print("Creating directory {}".format(filepath))
                os.makedirs(filepath)
            
            content = "\n    <!-- {} --> \n\n".format(sectionKey)
            for key, value in localization.items():
                androidKey = "{}.{}".format(sectionKey, key)
                if mockText:
                    content += makeAndroidEntry(androidKey, "{} - {}".format(mockString, value))
                elif longText:
                    content += makeAndroidEntry(androidKey, "{} - {}".format(longString, value))
                else:
                    content += makeAndroidEntry(androidKey, value)
        
            file = makeAndroidGeneratedWarning() + FileHelper.readFile("./templates/template_android_resource_file.txt").format(content)
            
            # Save file.
            FileHelper.writeFile(filename, file)

##### Main #####

def main(sourceFilenames, destinationDirectory, mockText, longText):
    
    # Construct destination paths.
    path = "{}/localization_gen".format(destinationDirectory)
    iosDestinationPath = "{}/ios".format(path)
    iosEnumDestinationPath = "{}/enum_swift".format(path)
    androidDestinationPath = "{}/android".format(path)
    
    # Create destination paths.
    createOrOverrideDirectory(path)
    createOrOverrideDirectory(iosDestinationPath)
    createOrOverrideDirectory(iosEnumDestinationPath)
    createOrOverrideDirectory(androidDestinationPath)
    
    # Process each source file.
    for source in sourceFilenames:
        filepath = checkSourceFilepath(source)
        dict = JsonHelper.readJSON(filepath)
        writeIOSStringResource(dict, iosDestinationPath, mockText, longText)
        writeIOSEnumFile(dict, iosEnumDestinationPath)
        writeAndroidStringResource(dict, androidDestinationPath, mockText, longText)
            
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
