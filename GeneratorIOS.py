import os

from lib import FileHelper

mockString = FileHelper.readFile("./templates/template_common_mock.txt")
longString = FileHelper.readFile("./templates/template_common_lorem.txt")

def makeIOSGeneratedWarning():
    warning = FileHelper.readFile("./templates/template_common_generated_warning.txt")
    return "/*\n{}\n */\n".format(warning)

def makeIOSEntry(key, value):
    value = value.replace("\"", "\\\"")
    value = value.replace("'", "\\'")
    return "\"{}\" = \"{}\";\n".format(key, value)

def writeIOSStringResource(dict, destinationDirectory, addMockText, addLongText):
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
                if addMockText:
                    content += makeIOSEntry(key, "{} - {}".format(mockString,value))
                elif addLongText:
                    content += makeIOSEntry(key, "{} - {}".format(longString,value))
                else:
                    content += makeIOSEntry(key, value)
            # Save file.
            FileHelper.writeFile(filename, content)
