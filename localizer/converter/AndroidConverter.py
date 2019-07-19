import os

from localizer.converter.ConverterInterface import ConverterInterface as Base
from localizer.lib import FileHelper
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

class AndroidConverter(Base):

    nameTagOpenStart = "<string name=\""
    nameTagOpenEnd = "\">"
    nameTagClose = "</string>"
    folderNamePrefix = "values-"

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self): return ".xml"

    def identifier(self): return "android" 

    def importDescription(self): return ""

    def exportDescription(self): return ""

    def toIntermediate(self, filepath):
        filename = FileHelper.filename(filepath)
        localizationIdentifier = filename.replace(self.fileExtension(), '')

        foldername = FileHelper.directoryName(filepath)
        languageIdentifier = foldername.replace(self.folderNamePrefix, '')

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []

        for line in lines: 
            entry = self._processLine(line, localizationIdentifier)
            if entry is not None:
                intermediateEntries.append(entry)
        
        intermediateLanguage = IntermediateLanguage(languageIdentifier, intermediateEntries)
        return IntermediateLocalization(localizationIdentifier, [intermediateLanguage])

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

    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------

    def _processLine(self, line, localizationIdentifier):
        if not self.nameTagOpenStart in line: 
            return None

        # remove leading whitespace
        while line.startswith(' '):
            line = line[1:]

        (key, line) = self._extractKey(line, localizationIdentifier)
        (value, line) = self._extractValue(line)
        
        return IntermediateEntry(key, value)

    def _extractKey(self, line, localizationIdentifier):
        # Remove start of name tag.
        if line.startswith(self.nameTagOpenStart):
            prefixLength = len(self.nameTagOpenStart)
            line = line[prefixLength:]

        # Remove name attribute and save it as key.
        key = ""
        while not line.startswith(self.nameTagOpenEnd):
            key += line[:1]
            line = line[1:]
        key = self._correctEntry(key)

        # This converter prefixes any generated android localization key with 'localizationIdentifier.'.
        # Remove them here to get a valid IntermediateEntry which is comparable and thus mergable.
        keyPrefix = "{}.".format(localizationIdentifier)
        key = key.replace(keyPrefix, '')

        # Remove end of name tag
        if line.startswith(self.nameTagOpenEnd):
            line = line[2:]

        return (key, line)

    def _extractValue(self, line):
        # Remove and save value until end of line.
        value = ""
        while not line.startswith(self.nameTagClose):
            value += line[:1]
            line = line[1:]
        value = self._correctEntry(value)
        value.replace("\"", "\\\"")
        return (value, line)

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

    def _makeAndroidGeneratedWarning(self):
        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        return "<!-- \n{} \n-->\n\n".format(warning)

    def _makeAndroidEntry(self, key, value):
        value = value.replace("\"", "\\\"")
        value = value.replace("'", "\\'")
        return "    <string name=\"{}\">{}</string>\n".format(key, value)
