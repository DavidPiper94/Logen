import unittest
import json

import os,sys,inspect
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from localizer.lib import FileHelper
from localizer.lib import JsonHelper

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.converter.JSONConverter import JSONConverter
from localizer.converter.iOSConverter import iOSConverter

class TestConverter(unittest.TestCase):

    def test_assertJSONStructure(self):
        """Assures equality between json and dict representation"""
        dict = JsonHelper.readJSON("localizer/tests/testdata/ExampleJSON.json")
        expectation = json.dumps(dict).replace('\n', '').replace(' ', '')

        exampleDict = self.helper_createExampleDict()
        result = json.dumps(exampleDict).replace(' ', '')

        self.assertEqual(expectation, result)

    def test_generateIntermediateFromJSON(self):
        """Assures equality between converted dict and expected intermediate representation"""
        expectation = self.helper_createExampleIntermediateLanguage()

        exampleDict = self.helper_createExampleDict()
        result = JSONConverter().toIntermediate("localizer/tests/testdata/ExampleJSON.json")
        
        self.assertEqual(expectation, result)

    def test_generateIntermediateFromiOS(self):
        expectation = self.helper_createExampleIntermediateLanguage()
        result = iOSConverter().toIntermediate("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
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
        expectedContent = FileHelper.readFile("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)

        exampleDict = self.helper_createExampleDict()
        intermediate = self.helper_createExampleIntermediateLanguage()
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