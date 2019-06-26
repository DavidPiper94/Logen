import unittest

from localizer.lib import FileHelper

from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

from localizer.converter.AndroidConverter import AndroidConverter

class TestAndroidConverter(unittest.TestCase):

    def test_generateIntermediateFromAndroid(self):
        pass

    def test_generateAndroidLocalization(self):
        expectedFilepath = "values-ExampleLanguage/FileName.xml"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/values-ExampleLanguage/FileName.xml")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLanguage()
        result = AndroidConverter().fromIntermediate(intermediate)[0]
        
        self.assertEqual(expectation, result)

    def _createExampleIntermediateLanguage(self):
        entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

if __name__ == '__main__':
    unittest.main()