import unittest

from localizer.lib import FileHelper
from localizer.lib import JsonHelper

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.converter.iOSConverter import iOSConverter

class TestiOSConverter(unittest.TestCase):

    #--------------------------------------------------
    # Testcases for main functionality
    #--------------------------------------------------

    def test_toIntermediate(self):
        expectation = self._createExampleIntermediateLocalization()
        result = iOSConverter().toIntermediate("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        self.assertEqual(expectation, result)

    def test_fromIntermediate(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLocalization()
        result = iOSConverter().fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Testcases for helper methods
    #--------------------------------------------------

    def test_extractKeyFromLine(self):
        line = "\"someKey\" = \"someValue\";"
        key = iOSConverter()._extractKeyFromLine(line)
        self.assertEqual("someKey", key)

    def test_correctKey(self):
        self.assertEqual("key", iOSConverter()._correctEntry("key"))
        self.assertEqual("key", iOSConverter()._correctEntry("   key"))
        self.assertEqual("key", iOSConverter()._correctEntry("key   "))
        self.assertEqual("key", iOSConverter()._correctEntry("\"key\""))
        self.assertEqual("key", iOSConverter()._correctEntry("   \"key\""))
        self.assertEqual("key", iOSConverter()._correctEntry("\"key\"   "))
        self.assertEqual("key", iOSConverter()._correctEntry("   \"key\"   "))

    def test_extractValueFromLine(self):
        line = "\"someKey\" = \"someValue\";"
        value = iOSConverter()._extractValueFromLine(line)
        self.assertEqual("someValue", value)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleIntermediateLocalization(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()