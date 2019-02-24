from lib import FileHelper

class LocalizationEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value

class LocalizationLanguage: 

    def __init__(self, languageIdentifier, localizationEntries):
        self.languageIdentifier = languageIdentifier
        self.localizationEntries = localizationEntries

class IntermediateLocalization:

    def __init__(self, localizationIdentifier, languages):
        self.localizationIdentifier = localizationIdentifier
        self.languages = languages

class LocalizationFile:

    def __init__(self, foldername, filename, filecontent):
        self.foldername = foldername
        self.filename = filename
        self.filecontent = filecontent

class Converter:

    def dictToIntermediateLocalization(self, dict):
        for sectionKey, sectionValue in dict.items():
            listOfLanguages = []
            for languageKey, localization in sectionValue.items():
                listOfEntries = []
                for key, value in localization.items():
                    entry = LocalizationEntry(key, value)
                    listOfEntries.append(entry)
                language = LocalizationLanguage(languageKey, listOfEntries)
                listOfLanguages.append(language)
            return IntermediateLocalization(sectionKey, listOfLanguages)

    def intermediateLocalizationToIosFiles(self, intermediateLocalization):
        listOfLocalizationFiles = []

        warning = FileHelper.readFile("./templates/template_common_generated_warning.txt")
        formattedWarning = "/*\n{}\n */\n".format(warning)

        for language in intermediateLocalization.languages:

            content = formattedWarning
            sectionHeaderTemplate = FileHelper.readFile("./templates/template_ios_section_header.txt")
            content += sectionHeaderTemplate.format(intermediateLocalization.localizationIdentifier)

            for entry in language.localizationEntries:
                value = entry.value.replace("\"", "\\\"").replace("'", "\\'")
                content += "\"{}\" = \"{}\";\n".format(entry.key, value)

            foldername = "{}.lproj".format(language.languageIdentifier)
            filename = "{}.strings".format(intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile(foldername, filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles