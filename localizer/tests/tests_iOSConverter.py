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
    # Testcases
    #--------------------------------------------------

    def test_toIntermediate(self):
        expectation = self._createExampleIntermediateLocalization()
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
        # TODO: Fix this test case:
        #self.assertEqual("This is a \"value\"", iOSConverter()._correctEntry("This is a \"value\""))

    def test_fromIntermediate(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLocalization()
        result = iOSConverter().fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleIntermediateLocalization(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()