from ConverterInterface import ConverterInterface as Base
from model import LocalizationFile
from lib import FileHelper

class iOSConverter(Base):

    def fileExtension(self): return ".strings"

    def toIntermediate(self, content):
        pass

    def fromIntermediate(self, intermediateLocalization):
        listOfLocalizationFiles = []

        warning = FileHelper.readFile("./templates/template_common_generated_warning.txt")
        formattedWarning = "/*\n{}\n */\n".format(warning)

        for language in intermediateLocalization.intermediateLanguages:

            content = formattedWarning
            sectionHeaderTemplate = FileHelper.readFile("./templates/template_ios_section_header.txt")
            content += sectionHeaderTemplate.format(intermediateLocalization.localizationIdentifier)

            for entry in language.intermediateEntries:
                value = entry.value.replace("\"", "\\\"").replace("'", "\\'")
                content += "\"{}\" = \"{}\";\n".format(entry.key, value)

            filename = "{}.lproj/{}.strings".format(language.languageIdentifier, intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile.LocalizationFile(filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles