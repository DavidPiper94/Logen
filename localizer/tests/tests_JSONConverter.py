import unittest

from localizer.lib import FileHelper
from localizer.lib import JsonHelper

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.converter.JSONConverter import JSONConverter

class TestJSONConverter(unittest.TestCase):

    def test_assertJSONStructure(self):
        """Assures equality between json and dict representation"""
        dict = JsonHelper.readJSON("localizer/tests/testdata/ExampleJSON.json")
        expectation = JsonHelper.dictToJSONString(dict).replace('\n', '').replace(' ', '')

        exampleDict = self.helper_createExampleDict()
        result = JsonHelper.dictToJSONString(exampleDict).replace(' ', '')

        self.assertEqual(expectation, result)

    def test_generateIntermediateFromJSON(self):
        """Assures equality between converted dict and expected intermediate representation"""
        expectation = self.helper_createExampleIntermediateLanguage()

        exampleDict = self.helper_createExampleDict()
        result = JSONConverter().toIntermediate("localizer/tests/testdata/ExampleJSON.json")
        
        self.assertEqual(expectation, result)

    def helper_createExampleDict(self):
        entriesDict = {}
        entriesDict["Key1"] = "Value1"

        languageDict = {}
        languageDict["ExampleLanguage"] = entriesDict

        fileDict = {}
        fileDict["FileName"] = languageDict
        return fileDict

    def helper_createExampleIntermediateLanguage(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()