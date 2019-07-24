import unittest

from localizer.converter.JSONConverter import JSONConverter
from localizer.lib import FileHelper, JsonHelper
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

class TestJSONConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = JSONConverter()

    #--------------------------------------------------
    # Testcases
    #--------------------------------------------------

    def test_assertJSONStructure(self):
        """Assures equality between json and dict representation"""
        dict = JsonHelper.readJSON("localizer/tests/testdata/ExampleJSON_noComments.json")
        expectation = JsonHelper.dictToJSONString(dict).replace('\n', '').replace(' ', '')

        exampleDict = self._createExampleDict()
        result = JsonHelper.dictToJSONString(exampleDict).replace(' ', '')

        self.assertEqual(expectation, result)

    def test_toIntermediate(self):
        """Assures equality between converted dict and expected intermediate representation"""
        expectation = self._createExampleIntermediateLocalization()
        result = self.sut.toIntermediate("localizer/tests/testdata/ExampleJSON_noComments.json")
        self.assertEqual(expectation, result)

    def test_fromIntermediate(self):
        """Assures equality between json dict created from intermediate localization and expected content of file."""
        expectedFilepath = "FileName.json"
        expectedContent = JsonHelper.readJSON("localizer/tests/testdata/ExampleJSON_noComments.json")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        localization = self._createExampleIntermediateLocalization()
        result = self.sut.fromIntermediate(localization)[0]
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleDict(self):
        entriesDict = {}
        entriesDict["Key1"] = "Value1"

        languageDict = {}
        languageDict["ExampleLanguage"] = entriesDict

        fileDict = {}
        fileDict["FileName"] = languageDict
        return fileDict

    def _createExampleIntermediateLocalization(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()
