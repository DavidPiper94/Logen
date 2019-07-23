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

    def changeFileExtensionTo(self, newFileExtension):
        self._fileExtension = newFileExtension

    def changeIdentifierTo(self, newIdentifier):
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

    def fileExtension(self): return self._fileExtension

    def identifier(self): return self._identifier

    def importDescription(self): raise NotImplementedError

    def exportDescription(self): raise NotImplementedError

    def toIntermediate(self, filepath: str) -> IntermediateLocalization: 
        self._didImport = True
        return None
        
    def fromIntermediate(self, intermediateLocalization: IntermediateLocalization) -> [LocalizationFile]: 
        self._didExport = True
        return []