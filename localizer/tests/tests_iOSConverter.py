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
        expectation = self._createExampleIntermediateLocalization(addComment = False)
        result = self.sut.toIntermediate("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        self.assertEqual(expectation, result, msg = self._errorMessageForIntermediateLocalization(expectation, result))

    def test_fromIntermediate(self):
        expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
        expectedContent = FileHelper.readFile("localizer/tests/testdata/ExampleLanguage.lproj/FileName.strings")
        expectation = LocalizationFile(expectedFilepath, expectedContent)
        intermediate = self._createExampleIntermediateLocalization(addComment = True)
        result = self.sut.fromIntermediate(intermediate)[0]
        self.assertEqual(expectation, result)

    # def test_fromIntermediate_noComments(self):
    #     expectedFilepath = "ExampleLanguage.lproj/FileName.strings"
    #     expectedContent = FileHelper.readFile("localizer/tests/testdata/ExampleLanguage.lproj/FileName_noComments.strings")
    #     expectation = LocalizationFile(expectedFilepath, expectedContent)
    #     intermediate = self._createExampleIntermediateLocalization(addComment = False)
    #     result = self.sut.fromIntermediate(intermediate)[0]
    #     self.assertEqual(expectation, result, msg = self._errorMessageForLocalizationFile(expectation, result))

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

    def _createExampleIntermediateLocalization(self, addComment: bool):
        if addComment:
            entry = IntermediateEntry("Key1", "Value1", "This is just a nonsence example.")
        else: 
            entry = IntermediateEntry("Key1", "Value1")
        language = IntermediateLanguage("ExampleLanguage", [entry])
        return IntermediateLocalization("FileName", [language])

    def _errorMessageForLocalizationFile(self, 
            expectation: LocalizationFile,
            actual: LocalizationFile) -> str:
        errorMessage = ""
        if expectation.filepath != actual.filepath:
            errorMessage += "Different filepath\n"
            errorMessage += "\t- expectation: {}\n".format(expectation.filepath)
            errorMessage += "\t- actual: {}\n".format(actual.filepath)
        if expectation.filecontent != actual.filecontent:
            errorMessage += "Different filecontent\n"
            errorMessage += "\t- expectation: {}\n".format(expectation.filecontent)
            errorMessage += "\t- actual: {}\n".format(actual.filecontent)
        return errorMessage

    def _errorMessageForIntermediateLocalization(self, 
            expectation: IntermediateLocalization, 
            actual: IntermediateLocalization) -> str:
        errorMessage = ""
        if expectation.localizationIdentifier != actual.localizationIdentifier:
            errorMessage += "Different localizationIdentifier\n"
            errorMessage += "\t- expectation: {}\n".format(expectation.localizationIdentifier)
            errorMessage += "\t- actual: {}\n".format(actual.localizationIdentifier)
        if expectation.intermediateLanguages != actual.intermediateLanguages:
            if len(expectation.intermediateLanguages) != len(actual.intermediateLanguages):
                errorMessage += "Different length of intermediate languages:\n"
                errorMessage += "\t- expectation: {}\n".format(len(expectation.intermediateLanguages))
                errorMessage += "\t- actual: {}\n".format(len(actual.intermediateLanguages))
            for index in range(0, min(len(expectation.intermediateLanguages), len(actual.intermediateLanguages))):
                errorMessage += self._errorMessageForIntermediateLanguage(expectation.intermediateLanguages[index], actual.intermediateLanguages[index])
        return errorMessage

    def _errorMessageForIntermediateLanguage(self, 
            expectation: IntermediateLanguage, 
            actual: IntermediateLanguage) -> str:
        errorMessage = ""
        if expectation.languageIdentifier != actual.languageIdentifier:
            errorMessage += "Different languageIdentifier\n"
            errorMessage += "\t- expectation: {}\n".format(expectation.languageIdentifier)
            errorMessage += "\t- actual: {}\n".format(actual.languageIdentifier)
        if expectation.intermediateEntries != actual.intermediateEntries:
            if len(expectation.intermediateEntries) != len(actual.intermediateEntries):
                errorMessage += "Different length of intermediateEntries:\n"
                errorMessage += "\t- expectation: {}\n".format(len(expectation.intermediateEntries))
                errorMessage += "\t- actual: {}\n".format(len(actual.intermediateEntries))
            for index in range(0, min(len(expectation.intermediateEntries), len(actual.intermediateEntries))):
                errorMessage += self._errorMessageForIntermediateEntry(expectation.intermediateEntries[index], actual.intermediateEntries[index])
        return errorMessage
    
    def _errorMessageForIntermediateEntry(self, 
            expectation: IntermediateEntry, 
            actual: IntermediateEntry) -> str:
        errorMessage = ""
        if expectation.key != actual.key:
            errorMessage += "Different key\n"
            errorMessage += "\t- expectation: {}\n".format(expectation.key)
            errorMessage += "\t- actual: {}\n".format(actual.key)
        if expectation.value != actual.value:
            errorMessage += "Different value\n"
            errorMessage += "\t- expectation: {}\n".format(expectation.value)
            errorMessage += "\t- actual: {}\n".format(actual.value)
        return errorMessage

if __name__ == '__main__':
    unittest.main()