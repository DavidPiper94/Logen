
import os

from localizer.converter.ConverterInterface import ConverterInterface as Base

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.lib import FileHelper

class AndroidConverter(Base):

    def fileExtension(self): return ".xml"

    def toIntermediate(self, filepath):
        filename = os.path.basename(filepath)
        localizationIdentifier = filename.replace('.xml', '')

        foldername = os.path.dirname(filepath).split('/')[-1]
        languageIdentifier = foldername.replace('values-', '')

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []

        for line in lines: 

            lineStart = "<string name=\""
            if not lineStart in line: 
                continue

            # remove leading whitespace
            while line.startswith(' '):
                line = line[1:]
            
            # Remove start of name tag.
            if line.startswith(lineStart):
                line = line[14:]

            # Remove name attribute and save it as key.
            key = ""
            while not line.startswith("\">"): #TODO: Nicht jede zeile endet so...
                key += line[:1]
                line = line[1:]
            key = self._correctEntry(key)

            # Remove end of name tag
            if line.startswith("\">"):
                line = line[2:]

            # Remove and save value until end of line.
            value = ""
            while not line.startswith("</string>"):
                value += line[:1]
                line = line[1:]
            value = self._correctEntry(value)
            value.replace("\"", "\\\"")
            intermediateEntries.append(IntermediateEntry(key, value))
        
        intermediateLanguage = IntermediateLanguage(languageIdentifier, intermediateEntries)
        return IntermediateLocalization(localizationIdentifier, [intermediateLanguage])

    def _correctEntry(self, input):
        entry = input
        while entry.startswith(' '):  # Remove leading whitespaces from key
            entry = entry[1:]
        if entry.startswith('\"'):    # Remove leading quote sign
            entry = entry[1:]
        while entry.endswith(' '):    # Remove trainling whitespaces from key
            entry = entry[:-1]
        if entry.endswith('\"'):      # Remove trailing quote sign
            entry = entry[:-1]
        return entry

    def fromIntermediate(self, intermediateLocalization):
        identifier = intermediateLocalization.localizationIdentifier
        languages = intermediateLocalization.intermediateLanguages
        listOfLocalizationFiles = []
        for language in languages:
            filename = "values-{}/{}.xml".format(language.languageIdentifier, identifier)
            content = "\n    <!-- {} --> \n\n".format(identifier)
            for entry in language.intermediateEntries:
                androidKey = "{}.{}".format(identifier, entry.key)
                content += self._makeAndroidEntry(androidKey, entry.value)

            filecontent = self._makeAndroidGeneratedWarning() + FileHelper.readFile("localizer/templates/template_android_resource_file.txt").format(content)
            localizationFile = LocalizationFile(filename, filecontent)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles

    def _makeAndroidGeneratedWarning(self):
        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        return "<!-- \n{} \n-->\n\n".format(warning)

    def _makeAndroidEntry(self, key, value):
        value = value.replace("\"", "\\\"")
        value = value.replace("'", "\\'")
        return "    <string name=\"{}\">{}</string>\n".format(key, value)