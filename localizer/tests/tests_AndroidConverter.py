import unittest

from localizer.converter.AndroidConverter import AndroidConverter
from localizer.lib import FileHelper
from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

class TestAndroidConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = AndroidConverter()

    #--------------------------------------------------
    # Testcases for main functionality
    #--------------------------------------------------

    def test_toIntermediate(self):
        expectation = self._createExampleIntermediateLanguage()
        result = self.sut.toIntermediate("localizer/tests/testdata/values-ExampleLanguage/FileName.xml")
        self.assertEqual(expectation, result)

    def test_fromIntermediate(self):
        expectedFilepath = "values-ExampleLanguage/FileName.xml"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/values-ExampleLanguage/FileName.xml")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLanguage()
        result = self.sut.fromIntermediate(intermediate)[0]
        
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Testcases for helper methods
    #--------------------------------------------------

    def test_processLine_validLine(self):
        line = "<string name=\"FileName.Key\">Value</string>"
        expectation = IntermediateEntry("Key", "Value")
        localizationIdentifier = "FileName"
        result = self.sut._processLine(line, localizationIdentifier)
        self.assertEqual(expectation, result)

    def test_processLine_validLine_leadingWhitespaces(self):
        expectation = IntermediateEntry("Key", "Value")
        line = "      <string name=\"FileName.Key\">Value</string>"
        localizationIdentifier = "FileName"
        result = self.sut._processLine(line, localizationIdentifier)
        self.assertEqual(expectation, result)
        
    def test_processLine_invalidLine(self):
        expectation = None
        line = "\"FileName.Key\"Value"
        localizationIdentifier = "FileName"
        result = self.sut._processLine(line, localizationIdentifier)
        self.assertEqual(expectation, result)

    def test_validLine(self):
        line = "<string name=\"FileName.Key\">Value</string>"
        self.assertTrue(self.sut._validLine(line))

    def test_validLine_missingStart(self):
        line = "\"FileName.Key\">Value</string>"
        self.assertFalse(self.sut._validLine(line))

    def test_validLine_missingEnd(self):
        line = "<string name=\"FileName.Key\">Value"
        self.assertFalse(self.sut._validLine(line))

    def test_extractKey(self):
        line = "<string name=\"FileName.Key\">Value</string>"
        localizationIdentifier = "FileName"
        (key, _) = self.sut._extractKey(line, localizationIdentifier)
        self.assertEqual("Key", key)

    def test_extractValue(self):
        line = "<string name=\"FileName.Key\">Value</string>"
        localizationIdentifier = "FileName"
        # Method _extractKey consumes start of line.
        # Thus this method needs to be called before the value can be extracted.
        (_, line) = self.sut._extractKey(line, localizationIdentifier)
        (value, _) = self.sut._extractValue(line)
        self.assertEqual("Value", value)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleIntermediateLanguage(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()
