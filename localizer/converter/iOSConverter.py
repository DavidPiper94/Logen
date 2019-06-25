import os

from ConverterInterface import ConverterInterface as Base

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.lib import FileHelper

class MergeResult():
    def __init__(self, mergedIntermediateLocalization, listOfMissingEntries):
        self.mergedIntermediateLocalization = mergedIntermediateLocalization
        self.listOfMissingEntries = listOfMissingEntries

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.mergedIntermediateLocalization == other.mergedIntermediateLocalization and self.listOfMissingEntries == other.listOfMissingEntries
    
    def __str__(self):
        description = "MergeResult of two IntermediateLoclaizations:\n" + str(self.mergedIntermediateLocalization) + "\nMissing Entries:"
        for entry in self.listOfMissingEntries:
            description += "{}, ".format(entry)
        return description

class iOSConverter(Base):

    def fileExtension(self): return ".strings"

    def toIntermediate(self, filepath):
        filename = os.path.basename(filepath)
        localizationIdentifier = filename.replace('.strings', '')

        foldername = os.path.dirname(filepath).split('/')[-1]
        languageIdentifier = foldername.replace('.lproj', '')

        lines = FileHelper.readLines(filepath)
        intermediateEntries = []
        for line in lines:
            if line.startswith("\""):
                key = line.split("=")[0]    # Split line between key and value TODO: This will not work, if there is a '=' in the Key!
                key = self._correctEntry(key)
                value = line.split("=", 1)[1][:-1] # Split string on first occurence of =, take second part and cut out last character (;)
                value = self._correctEntry(value)
                value.replace("\"", "\\\"")
                intermediateEntries.append(IntermediateEntry(key, value))

        intermediateLanguage = IntermediateLanguage(languageIdentifier, intermediateEntries)
        return IntermediateLocalization(localizationIdentifier, [intermediateLanguage])

    def _correctEntry(self, input):
        entry = input
        while entry.startswith(' '):  # Remove leading whitespaces from key
            entry = entry[1:]
        if entry.startswith('\"'):    # Remove leading quote sign
            entry = entry[1:]
        while entry.endswith(' '):    # Remove trainling whitespaces from key
            entry = entry[:-1]
        if entry.endswith('\"'):      # Remove trailing quote sign
            entry = entry[:-1]
        return entry

    # There may be cases, where it is useful to merge two intermediate localizations together.
    # E.g. when using this converter and there is one file de.lproj/File.strings and one en.lproj/File.strings,
    # Than the end result should be one single intermediate localization with both languages combined.
    # Another aproach would be to handle this case when importing a folder of multiple *.lproj directorys,
    # but this would need a special handling on importing. And how should other setups be handled?
    # Thus it is easier to add this method for merging two intermediate localizations together.
    # This method returns an instance of MergeResult.
    def _merge(self, first, second):

        # Make sure, both have the same identifier, else cancel.
        if first.localizationIdentifier is not second.localizationIdentifier:
            return None

        languages = first.intermediateLanguages + second.intermediateLanguages

        listOfMissingEntries = []
        for firstLanguage in first.intermediateLanguages:
            for secondLanguage in second.intermediateLanguages:
                listOfMissingEntries += self._compareEntries(firstLanguage.intermediateEntries, secondLanguage.intermediateEntries)

        return MergeResult(IntermediateLocalization(first.localizationIdentifier, languages), listOfMissingEntries)

    def _compareEntries(self, firstList, secondList):
        for item in firstList:
            if item in secondList:
                # Remove items, that are in both lists.
                firstList.remove(item)
                secondList.remove(item)

        # Return remainig items, which are only in one of both lists.
        return firstList + secondList

    def fromIntermediate(self, intermediateLocalization):
        listOfLocalizationFiles = []

        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        formattedWarning = "/*\n{}\n */\n".format(warning)

        for language in intermediateLocalization.intermediateLanguages:

            content = formattedWarning
            sectionHeaderTemplate = FileHelper.readFile("localizer/templates/template_ios_section_header.txt")
            content += sectionHeaderTemplate.format(intermediateLocalization.localizationIdentifier)

            for entry in language.intermediateEntries:
                value = entry.value.replace("\"", "\\\"").replace("'", "\\'")
                content += "\"{}\" = \"{}\";\n".format(entry.key, value)

            filename = "{}.lproj/{}.strings".format(language.languageIdentifier, intermediateLocalization.localizationIdentifier)
            localizationFile = LocalizationFile(filename, content)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles