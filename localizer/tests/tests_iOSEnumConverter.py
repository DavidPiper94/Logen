import unittest

from localizer.lib import FileHelper
from localizer.lib import JsonHelper

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.converter.iOSEnumConverter import iOSEnumConverter

class TestiOSEnumConverter(unittest.TestCase):

    # common subject under test for all test cases
    sut = iOSEnumConverter()

    #--------------------------------------------------
    # Testcases for main functionality
    #--------------------------------------------------

    # Method toIntermediate not tested, because this converter provides no import functionality.

    def test_fromIntermediate(self):
        expectedFilepath = "FileNameLocalizableKeys.swift"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/FileNameLocalizableKeys.swift")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLocalization()
        result = self.sut.fromIntermediate(intermediate)[0]
        self.assertEqual(expectation.filepath, result.filepath)

    #--------------------------------------------------
    # Private test helper
    #--------------------------------------------------

    def _createExampleIntermediateLocalization(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()