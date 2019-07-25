from localizer.model.IntermediateEntry import IntermediateEntry
from localizer.model.IntermediateLanguage import IntermediateLanguage
from localizer.model.IntermediateLocalization import IntermediateLocalization
from localizer.model.LocalizationFile import LocalizationFile

def createExampleIntermediateLocalization(addComment: bool):
    if addComment:
        entry = IntermediateEntry("Key1", "Value1", "This is just a nonsence example.")
    else: 
        entry = IntermediateEntry("Key1", "Value1")
    language = IntermediateLanguage("ExampleLanguage", [entry])
    return IntermediateLocalization("FileName", [language])

def errorMessageForLocalizationFile( 
        expectation: LocalizationFile,
        actual: LocalizationFile) -> str:
    errorMessage = ""
    if expectation.filepath != actual.filepath:
        errorMessage += "Different filepath\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.filepath)
        errorMessage += "\t- actual:      {}\n".format(actual.filepath)
    if expectation.filecontent != actual.filecontent:
        errorMessage += "Different filecontent\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.filecontent)
        errorMessage += "\t- actual:      {}\n".format(actual.filecontent)
    return errorMessage

def errorMessageForIntermediateLocalization( 
        expectation: IntermediateLocalization, 
        actual: IntermediateLocalization) -> str:
    errorMessage = ""
    if expectation.localizationIdentifier != actual.localizationIdentifier:
        errorMessage += "Different localizationIdentifier\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.localizationIdentifier)
        errorMessage += "\t- actual:      {}\n".format(actual.localizationIdentifier)
    if expectation.intermediateLanguages != actual.intermediateLanguages:
        if len(expectation.intermediateLanguages) != len(actual.intermediateLanguages):
            errorMessage += "Different length of intermediate languages:\n"
            errorMessage += "\t- expectation: {}\n".format(len(expectation.intermediateLanguages))
            errorMessage += "\t- actual:      {}\n".format(len(actual.intermediateLanguages))
        for index in range(0, min(len(expectation.intermediateLanguages), len(actual.intermediateLanguages))):
            errorMessage += errorMessageForIntermediateLanguage(expectation.intermediateLanguages[index], actual.intermediateLanguages[index])
    return errorMessage

def errorMessageForIntermediateLanguage( 
        expectation: IntermediateLanguage, 
        actual: IntermediateLanguage) -> str:
    errorMessage = ""
    if expectation.languageIdentifier != actual.languageIdentifier:
        errorMessage += "Different languageIdentifier\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.languageIdentifier)
        errorMessage += "\t- actual:      {}\n".format(actual.languageIdentifier)
    if expectation.intermediateEntries != actual.intermediateEntries:
        if len(expectation.intermediateEntries) != len(actual.intermediateEntries):
            errorMessage += "Different length of intermediateEntries:\n"
            errorMessage += "\t- expectation: {}\n".format(len(expectation.intermediateEntries))
            errorMessage += "\t- actual:      {}\n".format(len(actual.intermediateEntries))
        for index in range(0, min(len(expectation.intermediateEntries), len(actual.intermediateEntries))):
            errorMessage += errorMessageForIntermediateEntry(expectation.intermediateEntries[index], actual.intermediateEntries[index])
    return errorMessage

def errorMessageForIntermediateEntry( 
        expectation: IntermediateEntry, 
        actual: IntermediateEntry) -> str:
    errorMessage = ""
    if expectation.key != actual.key:
        errorMessage += "Different key\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.key)
        errorMessage += "\t- actual:      {}\n".format(actual.key)
    if expectation.value != actual.value:
        errorMessage += "Different value\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.value)
        errorMessage += "\t- actual:      {}\n".format(actual.value)
    if expectation.comment != actual.comment:
        errorMessage += "Different comment\n"
        errorMessage += "\t- expectation: {}\n".format(expectation.comment)
        errorMessage += "\t- actual:      {}\n".format(actual.comment)
    return errorMessage