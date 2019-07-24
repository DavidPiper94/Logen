import unittest

from localizer.lib import FileHelper
from localizer.lib import JsonHelper

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.converter.iOSConverter import iOSConverter

class TestiOSConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = iOSConverter()

    #--------------------------------------------------
    # Testcases for main functionality
    #--------------------------------------------------

    def test_toIntermediate(self):
        expectation = self._createExampleIntermediateLocalization()
        result = self.sut.toIntermediate("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        self.assertEqual(expectation, result)

    def test_fromIntermediate(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLocalization()
        result = self.sut.fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Testcases for helper methods
    #--------------------------------------------------

    def test_localizationIdentifierFromFilepath(self):
        filepath = "/some/filepath/de.lproj/TestIdentifier.strings"
        result = self.sut._localizationIdentifierFromFilepath(filepath)
        expectation = "TestIdentifier"
        self.assertEqual(expectation, result)

    def test_languageIdentifierFromFilepath(self):
        filepath = "/some/filepath/de.lproj/TestIdentifier.strings"
        result = self.sut._languageIdentifierFromFilepath(filepath)
        expectation = "de"
        self.assertEqual(expectation, result)

    def test_extractKeyFromLine(self):
        line = "\"someKey\" = \"someValue\";"
        key = self.sut._extractKeyFromLine(line)
        self.assertEqual("someKey", key)

    def test_correctKey(self):
        self.assertEqual("key", self.sut._correctEntry("key"))
        self.assertEqual("key", self.sut._correctEntry("   key"))
        self.assertEqual("key", self.sut._correctEntry("key   "))
        self.assertEqual("key", self.sut._correctEntry("\"key\""))
        self.assertEqual("key", self.sut._correctEntry("   \"key\""))
        self.assertEqual("key", self.sut._correctEntry("\"key\"   "))
        self.assertEqual("key", self.sut._correctEntry("   \"key\"   "))

    def test_extractValueFromLine(self):
        line = "\"someKey\" = \"someValue\";"
        value = self.sut._extractValueFromLine(line)
        self.assertEqual("someValue", value)

    def test__lineFromIntermediateEntry_WithComment(self):
        entry = IntermediateEntry("Key1", "Value1", "This is just a nonsence example.")
        expectation = "/* This is just a nonsence example. */\n\"Key1\" = \"Value1\";\n"
        result = self.sut._lineFromIntermediateEntry(entry)
        self.assertEqual(expectation, result)

    def test__lineFromIntermediateEntry_WithoutComment(self):
        entry = IntermediateEntry("Key1", "Value1")
        expectation = "\"Key1\" = \"Value1\";\n"
        result = self.sut._lineFromIntermediateEntry(entry)
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleIntermediateLocalization(self):
        entry = IntermediateEntry("Key1", "Value1", "This is just a nonsence example.")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()