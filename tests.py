import unittest
import json
import os

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

    def test_generateIntermediateFromJSON(self):
        """Assures equality between converted dict and expected intermediate representation"""
        expectation = self.helper_createExampleIntermediateLanguage()

        exampleDict = self.helper_createExampleDict()
        result = JSONConverter().toIntermediate("testdata/ExampleJSON.json")
        
        self.assertEqual(expectation, result)

    def test_generateIntermediateFromiOS(self):
        expectation = self.helper_createExampleIntermediateLanguage()
        result = iOSConverter().toIntermediate("testdata/ExampleLanguage.lproj/FileName.strings")
        self.assertEqual(expectation, result)

    def test_correctInput(self):
        self.assertEqual("key", iOSConverter()._correctEntry("key"))
        self.assertEqual("key", iOSConverter()._correctEntry("   key"))
        self.assertEqual("key", iOSConverter()._correctEntry("key   "))
        self.assertEqual("key", iOSConverter()._correctEntry("\"key\""))
        self.assertEqual("key", iOSConverter()._correctEntry("   \"key\""))
        self.assertEqual("key", iOSConverter()._correctEntry("\"key\"   "))
        self.assertEqual("key", iOSConverter()._correctEntry("   \"key\"   "))

    def test_generateIOS(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)

        exampleDict = self.helper_createExampleDict()
        intermediate = Converter().generateIntermediate(exampleDict)
        result = iOSConverter().fromIntermediate(intermediate)[0]
        
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