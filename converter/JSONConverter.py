from ConverterInterface import ConverterInterface as Base
from model.IntermediateEntry import IntermediateEntry
from model.IntermediateLanguage import IntermediateLanguage
from model.IntermediateLocalization import IntermediateLocalization
from lib import JsonHelper

class JSONConverter(Base):

    def fileExtension(self): return ".json"

    def toIntermediate(self, filepath):
        dict = JsonHelper.readJSON(filepath)
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

    def fromIntermediate(self, intermediateLocalization):
        pass