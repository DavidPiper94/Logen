# Import typing for adding type hints.
from typing import List, Optional, Tuple, Dict

# Import ConverterInterface as base class.
from ..converter.ConverterInterface import ConverterInterface as Base

# Import all needed model classes.
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

# Declaring class and inheriting from base converter.
class GroupingConverter(Base):

    # Implementing required functions to provide metadata.
    
    def fileExtension(self) -> str:
        # This converter will output a simple txt-file.
        return ".txt"

    def identifier(self) -> str: 
        # Specifies identifier with which it can be used from command line.
        return "grouping" 

    def importDescription(self) -> str: 
        # This description provide additional information on how this converter imports files. 
        # Since it will only support exporting, state this here.
        return "This converter does not support importing."

    def exportDescription(self) -> str: 
        # Gives a user more information of what this converter does when exporting.
        return "Groupes IntermediateEntry elements from different IntermediateLanguage elements by key."

    # Implement required import and export method.

    # Since it won't allow importing a file, raise an error.
    def toIntermediate(self, filepath: str) -> Optional[IntermediateLocalization]: raise NotImplementedError

    def fromIntermediate(
        self,
        intermediateLocalization: IntermediateLocalization
    ) -> List[LocalizationFile]:

        # An IntermediateLocalization contains a list of languages and each language has a list of entrys.
        # Since we want to group all translations by key, we need to restructure the data.
        # Each element in this dict will consist of the key of a translation and a list of tuples.
        # Each of this tuples in a list will have the languageIdentifier as well as the translation.
        keyDict: Dict[str, List[Tuple[str, str]]] = {}
        
        # Extract data from languages and restructure them in a better way for writing the output.
        for language in intermediateLocalization.intermediateLanguages:
            for entry in language.intermediateEntries:
                newTuple = (language.languageIdentifier, entry.value)
                if not entry.key in keyDict:
                    keyDict[entry.key] = []
                keyDict[entry.key].append(newTuple)

        # Now we have all translations in an easy accessable structure. Thus we can start to create the output.
        # Start with an empty string as content.
        content = ""

        for (key, listOfTuples) in keyDict.items():
            content += "Key: {}\n".format(key)
            for item in listOfTuples:
                content += "{}:\t{}\n".format(item[0], item[1])
            content += "\n"

        # This list will contain all files which will be returned. Start with an empty list.
        # For this converter the list will only contain a single file.
        listOfLocalizationFiles = []

        filename = "{}.txt".format(intermediateLocalization.localizationIdentifier)
        localizationFile = LocalizationFile(filename, content)
        listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles