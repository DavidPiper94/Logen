import unittest
import json
from IntermediateLocalization import Converter
from IntermediateLocalization import IntermediateEntry
from IntermediateLocalization import IntermediateLanguage
from IntermediateLocalization import IntermediateLocalization
from IntermediateLocalization import LocalizationFile

class TestConverter(unittest.TestCase):

    def test_assertJSONStructure(self):
        """Assures equality between json and dict representation"""
        expectation = """
        {
            "FileName": {
                "Language": {
                    "Key1": "Value1"
                }
            }
        }
        """.replace('\n', '').replace(' ', '')

        exampleDict = self.helper_createExampleDict()
        result = json.dumps(exampleDict).replace(' ', '')

        self.assertEqual(expectation, result)

    def test_generateIntermediate(self):
        """Assures equality between converted dict and expected intermediate representation"""
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("Language", [entry])
        intermediate = IntermediateLocalization("FileName", [language])
        print(intermediate)

        exampleDict = self.helper_createExampleDict()
        result = Converter().generateIntermediate(exampleDict)
        
        self.assertEqual(intermediate, result)

    def test_generateIOS(self):
        exampleDict = self.helper_createExampleDict()
        intermediate = Converter().generateIntermediate(exampleDict)
        result = Converter().generateIOS(intermediate)

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