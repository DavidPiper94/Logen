from lib import FileHelper
import abc
from model.IntermediateEntry import IntermediateEntry
from model.IntermediateLanguage import IntermediateLanguage
from model.IntermediateLocalization import IntermediateLocalization
from model.LocalizationFile import LocalizationFile

# ==============================
# Internal input to generator
# ==============================

# ==============================
# Generator
# ==============================

class Converter:

    def generateIntermediate(self, dict):
        for sectionKey, sectionValue in dict.items():
            listOfLanguages = []
            for languageKey, localization in sectionValue.items():
                listOfEntries = []
                for key, value in localization.items():
                    entry = IntermediateEntry(key, value)
                    listOfEntries.append(entry)
                language = IntermediateLanguage(languageKey, listOfEntries)
                listOfLanguages.append(language)
            return IntermediateLocalization(sectionKey, listOfLanguages)

    def generateIOSEnum(self, intermediateLocalization):

        # The enum keys are independet of the language. Thus just handel the first language.
        language = intermediateLocalization.intermediateLanguages[0]

        warning = FileHelper.readFile("./templates/template_common_generated_warning.txt")
        formattedWarning = "/*\n{}\n */\n".format(warning)
        content = formattedWarning
        content += FileHelper.readFile("./templates/template_ios_base_class_import.txt")
        content += FileHelper.readFile("./templates/template_ios_enum_documentation.txt")
        content += "extension LocalizableKeys {\n"
        content += "    enum {0}: String {{\n".format(intermediateLocalization.localizationIdentifier)
        for entry in language.intermediateEntries:
            key = entry.key.replace(".", "_")
            content += "        case {} = \"{}\"\n".format(key, entry)
        content += "    }\n"
        content += "}"

        foldername = ""
        # Create filename.
        # This line capitalizes the first letter in the sectionKey.
        # This is used as part of the filename, so it will be capitalizesd as it should be.
        # We can't use .capitalize() or .title() because that would lowercase all other chars.
        sectionName = ' '.join(word[0].upper() + word[1:] for word in intermediateLocalization.localizationIdentifier.split())
        filename = "{}LocalizableKeys.swift".format(sectionName)
        localizationFile = LocalizationFile(foldername, filename, content)
        return localizationFile