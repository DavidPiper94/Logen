import unittest

from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

from ..converter.GroupingConverter import GroupingConverter

from ..tests import TestHelper

class TestGroupingConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = GroupingConverter()

    #--------------------------------------------------
    # Test
    #--------------------------------------------------

    def testTest(self):
        expectation = self._createExpectedOutput()
        intermediate = self._createMultiLanguageIntermediateLocalization()
        result = self.sut.fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result, msg = TestHelper.errorMessageForLocalizationFile(expectation, result))

    #--------------------------------------------------
    # Helper for Tests
    #--------------------------------------------------

    def _createMultiLanguageIntermediateLocalization(self) -> IntermediateLocalization:
        # Create first language, e.g. English
        enEntry1 = IntermediateEntry("Key1", "Value in English")
        enEntry2 = IntermediateEntry("Key2", "Another value in English")
        enLanguage = IntermediateLanguage("en", [enEntry1, enEntry2])

        # Create second language, e.g. German
        deEntry1 = IntermediateEntry("Key1", "Value in German")
        deEntry2 = IntermediateEntry("Key2", "Another value in German")
        deLanguage = IntermediateLanguage("de", [deEntry1, deEntry2])

        # Create third language, e.g. Spanish
        esEntry1 = IntermediateEntry("Key1", "Value in Spanish")
        esEntry2 = IntermediateEntry("Key2", "Another value in Spanish")
        esLanguage = IntermediateLanguage("es", [esEntry1, esEntry2])

        return IntermediateLocalization("Example", [enLanguage, deLanguage, esLanguage])

    def _createExpectedOutput(self) -> LocalizationFile:
        expectedFilepath = "Example.txt"
        expectedContent = """Key: Key1
en:\tValue in English
de:\tValue in German
es:\tValue in Spanish

Key: Key2
en:\tAnother value in English
de:\tAnother value in German
es:\tAnother value in Spanish

"""
        return LocalizationFile(expectedFilepath, expectedContent)

if __name__ == '__main__':
    unittest.main()