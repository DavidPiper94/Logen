from localizer.converter.ConverterInterface import ConverterInterface as Base
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile
from localizer.lib import JsonHelper

class JSONConverter(Base):

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self): return ".json"

    def identifier(self): return "json"

    def toIntermediate(self, filepath):
        dict = JsonHelper.readJSON(filepath)

        # JsonHelper could not read json file at given path.
        if dict is None:
            return None

        for sectionKey, sectionValue in dict.items():

            listOfLanguages = []

            # Check for correct format of json.
            if not type(sectionValue) is type({}):
                return None

            for languageKey, localization in sectionValue.items():
                listOfEntries = []
                for key, value in localization.items():
                    entry = IntermediateEntry(key, value)
                    listOfEntries.append(entry)
                language = IntermediateLanguage(languageKey, listOfEntries)
                listOfLanguages.append(language)
            return IntermediateLocalization(sectionKey, listOfLanguages)

    def fromIntermediate(self, intermediateLocalization):
        localizationFiles = []

        localizationDict = {}
        languageDict = {}
        for language in intermediateLocalization.intermediateLanguages:

            entryDict = {}
            for entry in language.intermediateEntries:
                entryDict[entry.key] = entry.value
            
            languageDict[language.languageIdentifier] = entryDict
            localizationDict[intermediateLocalization.localizationIdentifier] = languageDict

            filename = "{}{}".format(intermediateLocalization.localizationIdentifier, self.fileExtension())
            localizationFile = LocalizationFile(filename, localizationDict)
            localizationFiles.append(localizationFile)
        
        return localizationFiles