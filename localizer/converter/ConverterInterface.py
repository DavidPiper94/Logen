import abc

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile
from localizer.model.MergeResult import MergeResult

class ConverterInterface:

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def fileExtension(self): raise NotImplementedError

    @abc.abstractproperty
    def identifier(self): raise NotImplementedError

    @abc.abstractmethod
    def toIntermediate(self, filepath: str) -> IntermediateLocalization:
        """Reads content of file at given filepath and converts it to an IntermediateLocalization.
        
        Parameters
        ----------
        filepath: str
            Path to file which content will be converted.

        Returns
        -------
        LocalizationFile:
            Instance of class IntermediateLocalization containing the converted content of the file.

        Raises
        ------
        NotImplementedError
            If no converting method is available for the content.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def fromIntermediate(self, intermediateLocalization: IntermediateLocalization) -> LocalizationFile: 
        """Converts intermediate localization to specific format.
        
        Parameters
        ----------
        intermediateLocalization: IntermediateLocalization
            The intermediate localization to be converted.

        Returns
        -------
        LocalizationFile:
            Instance of class LocalizationFile encapsulating filepath and content.

        Raises
        ------
        NotImplementedError
            If no converting method is available for this intermediate localization.
        """

        raise NotImplementedError

    # There may be cases, where it is useful to merge two intermediate localizations together.
    # E.g. when using this converter and there is one file de.lproj/File.strings and one en.lproj/File.strings,
    # Than the end result should be one single intermediate localization with both languages combined.
    # Another aproach would be to handle this case when importing a folder of multiple *.lproj directorys,
    # but this would need a special handling on importing. And how should other setups be handled?
    # Thus it is easier to add this method for merging two intermediate localizations together.
    # This method returns an instance of MergeResult.
    def merge(self, first: IntermediateLocalization, second: IntermediateLocalization) -> IntermediateLocalization:

        # Make sure, both are objects of type IntermeditateLocalization.
        if not type(first) is IntermediateLocalization or not type(second) is IntermediateLocalization:
            return None

        # Make sure, both have the same identifier, else cancel.
        if not first.localizationIdentifier == second.localizationIdentifier:
            return None

        languages = first.intermediateLanguages + second.intermediateLanguages

        listOfMissingEntries = []
        for firstLanguage in first.intermediateLanguages:
            for secondLanguage in second.intermediateLanguages:
                listOfMissingEntries += self._compareEntries(firstLanguage.intermediateEntries, secondLanguage.intermediateEntries)

        return MergeResult(IntermediateLocalization(first.localizationIdentifier, languages), listOfMissingEntries)

    def _compareEntries(self, firstList, secondList):
        for item in firstList[:]:
            if item in secondList:
                # Remove items, that are in both lists.
                firstList = list(filter(lambda x: x != item, firstList))
                secondList = list(filter(lambda x: x != item, secondList))

        # Return remainig items, which are only in one of both lists.
        return firstList + secondList
