# This python script converts the localizable file at the given path and converts it to a common json file which can be converted into the android localization.

import json

sourcePath = "/Users/davidpiper/Documents/Developer/Nina/native_ios/NINA/Localizable.strings"
destinationPath = "/Users/davidpiper/Desktop/localization.json"

lines = open(sourcePath).read().split("\n")

content = "{\n"
content += "    \"localization\": {\n"
content += "        \"de\": {\n"

for line in lines:
    if line.startswith("\""):
        key = line.split("=")[0]
        value = line.split("=", 1)[1][:-1] # Split string on first occurence of =, take second part and cut out last character (;)
        value.replace("\"", "\\\"")
        content += "            {}: {},\n".format(key, value)

content = content[:-2] # remove last , from for loop together with \n
content += "\n" # add \n cutted by previous line again
content += "        }\n"
content += "    }\n"
content += "}"

textFile = open(destinationPath, "w")
textFile.write(content)
textFile.close()
