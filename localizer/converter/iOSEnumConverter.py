import os

from localizer.converter.ConverterInterface import ConverterInterface as Base
from localizer.lib import FileHelper
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

class iOSEnumConverter(Base):

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self): return ".swift"

    def identifier(self): return "ios_enum"

    def importDescription(self): return "No import possible."

    def exportDescription(self): return "Exports the content of an intermediate localization to a swift enum providing easy and convenience access to the keys."

    def toIntermediate(self, filepath): raise NotImplementedError
        
    def fromIntermediate(self, intermediateLocalization):
        listOfLocalizationFiles = []

        content = self._makeiOSGeneratedWarning()
        content += FileHelper.readFile("localizer/templates/template_ios_enum_documentation.txt")

        filename = self._makeFilename(intermediateLocalization.localizationIdentifier)

        # Keys are equal for every language, thus just use the first one.
        language = intermediateLocalization.intermediateLanguages[0]

        content += "extension LocalizableKeys {\n"
        content += "    enum {0}: String {{\n".format(intermediateLocalization.localizationIdentifier)
        for entry in language.intermediateEntries:
            content += self._makeIOSEnumEntry(entry.key)
        content += "    }\n"
        content += "}"

        localizationFile = LocalizationFile(filename, content)
        listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles
        
    #--------------------------------------------------
    # Helper methods
    #--------------------------------------------------

    def _makeiOSGeneratedWarning(self):
        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        return "/*\n{}\n */\n".format(warning)

    def _makeFilename(self, sectionKey: str) -> str:
        # This line capitalizes the first letter in the sectionKey.
        # This is used as part of the filename, so it will be capitalizesd as it should be.
        # We can't use .capitalize() or .title() because that would lowercase all other chars.
        sectionName = ' '.join(word[0].upper() + word[1:] for word in sectionKey.split())
        return "{}LocalizableKeys.swift".format(sectionName)

    def _makeIOSEnumEntry(self, key):
        newKey = key.replace(".", "_")
        return "        case {} = \"{}\"\n".format(newKey, key)