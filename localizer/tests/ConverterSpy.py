from typing import List, Optional

from localizer.converter.ConverterInterface import ConverterInterface as Base
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

class ConverterSpy(Base):    
    
    #--------------------------------------------------
    # private properties
    #--------------------------------------------------

    _fileExtension = ""
    _identifier = ""

    _didImport = False
    _didExport = False

    #--------------------------------------------------
    # Methods to change functionality
    #--------------------------------------------------

    def changeFileExtensionTo(self, newFileExtension: str) -> None:
        self._fileExtension = newFileExtension

    def changeIdentifierTo(self, newIdentifier: str) -> None:
        self._identifier = newIdentifier

    #--------------------------------------------------
    # Methods to check functionality
    #--------------------------------------------------

    def didImport(self) -> bool:
        return self._didImport

    def didExport(self) -> bool:
        return self._didExport

    #--------------------------------------------------
    # Base class conformance
    #--------------------------------------------------

    def fileExtension(self) -> str: return self._fileExtension

    def identifier(self) -> str: return self._identifier

    def importDescription(self) -> str: raise NotImplementedError

    def exportDescription(self) -> str: raise NotImplementedError

    def toIntermediate(
        self, 
        filepath: str
    ) -> Optional[IntermediateLocalization]: 

        self._didImport = True
        # Return empty IntermediateLocalization, because the subcommand convert checks if the returned Intermediate localization is none.
        # When returning none, the subcommand convert won't continue in tests.
        return IntermediateLocalization("", [])
        
    def fromIntermediate(
        self, 
        intermediateLocalization: IntermediateLocalization
    ) -> List[LocalizationFile]: 

        self._didExport = True
        return []