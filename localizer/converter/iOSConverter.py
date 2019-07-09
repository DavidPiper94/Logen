import os

from localizer.converter.ConverterInterface import ConverterInterface as Base

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.lib import FileHelper

class iOSConverter(Base):

    def fileExtension(self): return ".strings"

    def toIntermediate(self, filepath):
        filename = os.path.basename(filepath)
        localizationIdentifier = filename.replace('.strings', '')

        foldername = os.path.dirname(filepath).split('/')[-1]
        languageIdentifier = foldername.replace('.lproj', '')

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []
        for line in lines:
            if line.startswith("\""):
                key = line.split("=")[0]    # Split line between key and value TODO: This will not work, if there is a '=' in the Key!
                key = self._correctEntry(key)
                value = line.split("=", 1)[1][:-1] # Split string on first occurence of =, take second part and cut out last character (;)
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
        listOfLocalizationFiles = []

        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        formattedWarning = "/*\n{}\n */\n".format(warning)
        sectionHeaderTemplate = FileHelper.readFile("localizer/templates/template_ios_section_header.txt")

        for language in intermediateLocalization.intermediateLanguages:

            content = formattedWarning
            content += sectionHeaderTemplate.format(intermediateLocalization.localizationIdentifier)

            for entry in language.intermediateEntries:
                value = entry.value.replace("\"", "\\\"").replace("'", "\\'")
                content += "\"{}\" = \"{}\";\n".format(entry.key, value)

            filename = "{}.lproj/{}.strings".format(language.languageIdentifier, intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile(filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles