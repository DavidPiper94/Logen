import unittest

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile
from localizer.model.MergeResult import MergeResult

from localizer.converter.iOSConverter import iOSConverter

class TestJSONConverter(unittest.TestCase):

    def test_merge_differentLocalizationIdentifier(self):
        example = IntermediateLocalization("Example", [])
        otherExample = IntermediateLocalization("OtherExample", [])

        # Using an abritary converter class to test common merge functionality.
        result = iOSConverter().merge(example, otherExample)

        self.assertEqual(result, None)

    def test_merge_equalEntries(self):
        (example, otherExample) = self._createExampleIntermediateLocalizations()

        # Using an abritary converter class to test common merge functionality.
        result = iOSConverter().merge(example, otherExample)

        listOfLanguageIdentifier = []
        for intermediateLanguage in result.mergedIntermediateLocalization.intermediateLanguages:
            listOfLanguageIdentifier.append(intermediateLanguage.languageIdentifier)

        self.assertEqual(sorted(listOfLanguageIdentifier), sorted(["de", "en"]))
        self.assertEqual(result.listOfMissingEntries, [])

    def test_merge_unequalEntries(self):
        example, otherExample = self._createExampleIntermediateLocalizations()

        example.intermediateLanguages[0].intermediateEntries.append(IntermediateEntry("FirstNewKey", "FirstNewValue"))
        otherExample.intermediateLanguages[0].intermediateEntries.append(IntermediateEntry("SecondNewKey", "SecondNewValue"))

        # Using an abritary converter class to test common merge functionality.
        newResult = iOSConverter().merge(example, otherExample)

        self.assertEqual(newResult.listOfMissingEntries, [IntermediateEntry("FirstNewKey", "FirstNewValue"), IntermediateEntry("SecondNewKey", "SecondNewValue")])
    
    def _createExampleIntermediateLocalizations(self):
        entry = IntermediateEntry("Key1", "Value1")
        
        germanLanguage = IntermediateLanguage("de", [entry])
        example = IntermediateLocalization("FileName", [germanLanguage])

        englishLanguage = IntermediateLanguage("en", [entry])
        otherExample = IntermediateLocalization("FileName", [englishLanguage])
        
        return (example, otherExample)

if __name__ == '__main__':
    unittest.main()