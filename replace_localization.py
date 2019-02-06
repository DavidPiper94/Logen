import sys
import json         # for processing the json files
import glob         # for extracting all filenames from the given source directory

def readJSON(filepath):
    with open(filepath) as file:
        data = json.load(file)
        return data.items()

# Writes given content to given filepath.
def writeFile(filepath, content):
    textFile = open(filepath, "w")
    textFile.write(content)
    textFile.close()

def readFile(filepath): 
    textFile = open(filepath, "r")
    content = textFile.read()
    textFile.close()
    return content

##### Main #####

def main(localizationFiles, codeFiles):
    for localizationFile in localizationFiles:
        for codeFile in codeFiles:
            content = readFile(codeFile)
            dict = readJSON(localizationFile)

            for sectionKey, sectionValue in dict:
                for languageKey, localization in sectionValue.items():
                    for key, value in localization.items():
                        if value in content:
                            new = "Localizer.string(forKey: LocalizableKeys.{}.{}.rawValue)!".format(sectionKey, key)
                            replacable = "\"{}\"".format(value)
                            content = content.replace(replacable, new)

            writeFile(codeFile, content)
    
if __name__ == "__main__":

    # get all json files from source directory
    localizationSourceDirectory = sys.argv[1]
    localizationFilenames = []
    for localizationFile in glob.glob("{}/*.json".format(localizationSourceDirectory)):
        localizationFilenames.append(localizationFile)

    # select all swift files up to the sub-sub-sub-sub-directory of given project directory
    projectSourceDirectory = sys.argv[2]
    codeFilenames = []
    for codeFile in glob.glob("{}/*.swift".format(projectSourceDirectory)):
        codeFilenames.append(codeFile)
    for codeFile in glob.glob("{}/*/*.swift".format(projectSourceDirectory)):
        codeFilenames.append(codeFile)
    for codeFile in glob.glob("{}/*/*/*.swift".format(projectSourceDirectory)):
        codeFilenames.append(codeFile)
    for codeFile in glob.glob("{}/*/*/*/*.swift".format(projectSourceDirectory)):
        codeFilenames.append(codeFile)

    # start main function
    main(localizationFilenames, codeFilenames)
