from lib import FileHelper

# ==============================
# Internal input to generator
# ==============================

class IntermediateEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.key == other.key and self.value == other.value

    def __str__(self):
        return "   IntermediateEntry: " + self.key + ": " + self.value

class IntermediateLanguage: 

    def __init__(self, languageIdentifier, intermediateEntries):
        self.languageIdentifier = languageIdentifier
        self.intermediateEntries = intermediateEntries
        
    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.languageIdentifier == other.languageIdentifier and self.intermediateEntries == other.intermediateEntries

    def __str__(self):
        description = "IntermediateLanguage:\n   LanguageIdentifier: {}\n".format(self.languageIdentifier)
        for entry in self.intermediateEntries:
            description += str(entry)
        return description

class IntermediateLocalization:

    def __init__(self, localizationIdentifier, intermediateLanguages):
        self.localizationIdentifier = localizationIdentifier
        self.intermediateLanguages = intermediateLanguages

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.localizationIdentifier == other.localizationIdentifier and self.intermediateLanguages == other.intermediateLanguages

    def __str__(self):
        description = "IntermediateLocalization:\nLocalizationIdentifier: {}\n".format(self.localizationIdentifier)
        for language in self.intermediateLanguages:
            description += str(language)
        return description

# ==============================
# Internal output of generator
# ==============================

class LocalizationFile:

    def __init__(self, foldername, filename, filecontent):
        self.foldername = foldername
        self.filename = filename
        self.filecontent = filecontent

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.foldername == other.foldername and self.filename == other.filename and self.filecontent == other.filecontent

    def __str__(self):
         return "LocalizationFile:\nFolder: {}\nFilename: {}\nContent: {}".format(self.foldername, self.filename, self.filecontent)

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

    def generateIOS(self, intermediateLocalization):
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

            foldername = "{}.lproj".format(language.languageIdentifier)
            filename = "{}.strings".format(intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile(foldername, filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles

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