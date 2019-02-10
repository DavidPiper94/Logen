import os

from lib import FileHelper

def makeIOSGeneratedWarning():
    warning = FileHelper.readFile("./templates/template_common_generated_warning.txt")
    return "/*\n{}\n */\n".format(warning)

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
            content += FileHelper.readFile("./templates/template_ios_base_class_import.txt")
            content += FileHelper.readFile("./templates/template_ios_enum_documentation.txt")
            content += "extension LocalizableKeys {\n"
            content += "    enum {0}: String {{\n".format(sectionKey)
            for key, value in localization.items():
                content += makeIOSEnumEntry(key)
            content += "    }\n"
            content += "}"

    FileHelper.writeFile(filename, content)