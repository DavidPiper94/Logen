from ConverterInterface import ConverterInterface as Base
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.lib import JsonHelper

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