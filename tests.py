import unittest
import json

from lib import FileHelper
from lib import JsonHelper

from IntermediateLocalization import Converter
from model.IntermediateEntry import IntermediateEntry
from model.IntermediateLanguage import IntermediateLanguage
from model.IntermediateLocalization import IntermediateLocalization
from model.LocalizationFile import LocalizationFile

from converter.JSONConverter import JSONConverter
from converter.iOSConverter import iOSConverter

class TestConverter(unittest.TestCase):

    def test_assertJSONStructure(self):
        """Assures equality between json and dict representation"""
        dict = JsonHelper.readJSON("testdata/ExampleJSON.json")
        expectation = json.dumps(dict).replace('\n', '').replace(' ', '')

        exampleDict = self.helper_createExampleDict()
        result = json.dumps(exampleDict).replace(' ', '')

        self.assertEqual(expectation, result)

    def test_generateIntermediate(self):
        """Assures equality between converted dict and expected intermediate representation"""
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("Language", [entry])
        intermediate = IntermediateLocalization("FileName", [language])

        exampleDict = self.helper_createExampleDict()
        result = JSONConverter().toIntermediate("testdata/ExampleJSON.json")
        
        self.assertEqual(intermediate, result)

    def test_generateIOS(self):
        expectedFilepath = "Language.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("testdata/ExpectedStringsContent.txt")
        expectation = LocalizationFile(expectedFilepath, expectedContent)

        exampleDict = self.helper_createExampleDict()
        intermediate = Converter().generateIntermediate(exampleDict)
        result = iOSConverter().fromIntermediate(intermediate)[0]
        
        self.assertEqual(expectation, result)

    def helper_createExampleDict(self):
        entriesDict = {}
        entriesDict["Key1"] = "Value1"

        languageDict = {}
        languageDict["Language"] = entriesDict

        fileDict = {}
        fileDict["FileName"] = languageDict
        return fileDict

if __name__ == '__main__':
    unittest.main()