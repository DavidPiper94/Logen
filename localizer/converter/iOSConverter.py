import os

from localizer.converter.ConverterInterface import ConverterInterface as Base
from localizer.lib import FileHelper
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

class iOSConverter(Base):

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self): return ".strings"

    def identifier(self): return "ios"

    def importDescription(self): return "Imports a '.strings' file containing the localization of an iOS app and converts it to an intermediate localization. Ignores all lines exept lines with a key-value-pair."

    def exportDescription(self): return "Exports the content of an intermediate localization to a '.strings' file for an iOS app."

    def toIntermediate(self, filepath):
        localizationIdentifier = self._localizationIdentifierFromFilepath(filepath)
        languageIdentifier = self._languageIdentifierFromFilepath(filepath)

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []

        # A line may or may not contain a comment. Start with an empty string as default.
        comment = ""

        for line in lines:
            if line.startswith("//") or (line.startswith("/*") and line.endswith("*/")):
                # The next line may containe a entry with a comment.
                comment = self._extractCommentFromLine(line)
                continue

            if line.startswith("\""):
                key = self._extractKeyFromLine(line)
                value = self._extractValueFromLine(line)
                intermediateEntries.append(IntermediateEntry(key, value, comment))

                # Reset value of comment for next line.
                comment = ""

        intermediateLanguage = IntermediateLanguage(languageIdentifier, intermediateEntries)
        return IntermediateLocalization(localizationIdentifier, [intermediateLanguage])

    def fromIntermediate(self, intermediateLocalization):
        listOfLocalizationFiles = []

        content = self._makeiOSGeneratedWarning()
        sectionHeaderTemplate = FileHelper.readFile("localizer/templates/template_ios_section_header.txt")

        for language in intermediateLocalization.intermediateLanguages:

            content += sectionHeaderTemplate.format(intermediateLocalization.localizationIdentifier)

            for entry in language.intermediateEntries:
                content += self._lineFromIntermediateEntry(entry)

            filename = "{}.lproj/{}.strings".format(language.languageIdentifier, intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile(filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles

    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------
    
    def _localizationIdentifierFromFilepath(self, filepath: str) -> str:
        filename = os.path.basename(filepath)
        return filename.replace(".strings", "")

    def _languageIdentifierFromFilepath(self, filepath: str) -> str:
        foldername = os.path.dirname(filepath).split("/")[-1]
        return foldername.replace(".lproj", "")

    def _extractCommentFromLine(self, line: str) -> str:
        comment = self._correctEntry(line)
        # TODO:
        comment = "This is just a nonsence example."
        return comment

    def _extractKeyFromLine(self, line):
        key = line.split("=")[0]    # Split line between key and value TODO: This will not work, if there is a "="" in the Key!
        key = self._correctEntry(key)
        return key

    def _extractValueFromLine(self, line):
        value = line.split("=", 1)[1][:-1] # Split string on first occurence of =, take second part and cut out last character (;)
        value = self._correctEntry(value)
        value.replace("\"", "\\\"")
        return value

    def _correctEntry(self, input):
        entry = input
        while entry.startswith(" "):  # Remove leading whitespaces from key
            entry = entry[1:]
        if entry.startswith("\""):    # Remove leading quote sign
            entry = entry[1:]
        while entry.endswith(" "):    # Remove trainling whitespaces from key
            entry = entry[:-1]
        if entry.endswith("\""):      # Remove trailing quote sign
            entry = entry[:-1]
        return entry

    def _makeiOSGeneratedWarning(self):
        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        return "/*\n{}\n */\n".format(warning)

    def _lineFromIntermediateEntry(self, entry: IntermediateEntry) -> str:
        # add comment
        line = ""
        if entry.comment != "":
            line += "/* {} */\n".format(entry.comment)
        value = entry.value.replace("\"", "\\\"").replace("'", "\\'")
        line += "\"{}\" = \"{}\";\n".format(entry.key, value)
        return line