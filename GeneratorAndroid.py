import os

from lib import FileHelper

def makeAndroidGeneratedWarning():
    warning = FileHelper.readFile("./templates/template_common_generated_warning.txt")
    return "<!-- \n{} \n-->\n\n".format(warning)

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
