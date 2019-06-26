from ConverterInterface import ConverterInterface as Base

from localizer.model.LocalizationFile import LocalizationFile

from localizer.lib import FileHelper

class AndroidConverter(Base):

    def fileExtension(self): return ".xml"

    def toIntermediate(self, filepath):
        pass

    def fromIntermediate(self, intermediateLocalization):
        identifier = intermediateLocalization.localizationIdentifier
        languages = intermediateLocalization.intermediateLanguages
        listOfLocalizationFiles = []
        for language in languages:
            filename = "values-{}/{}.xml".format(language.languageIdentifier, identifier)
            content = "\n    <!-- {} --> \n\n".format(identifier)
            for entry in language.intermediateEntries:
                androidKey = "{}.{}".format(identifier, entry.key)
                content += self._makeAndroidEntry(androidKey, entry.value)

            filecontent = self._makeAndroidGeneratedWarning() + FileHelper.readFile("localizer/templates/template_android_resource_file.txt").format(content)
            localizationFile = LocalizationFile(filename, filecontent)
            listOfLocalizationFiles.append(localizationFile)

        return listOfLocalizationFiles

    def _makeAndroidGeneratedWarning(self):
        warning = FileHelper.readFile("localizer/templates/template_common_generated_warning.txt")
        return "<!-- \n{} \n-->\n\n".format(warning)

    def _makeAndroidEntry(self, key, value):
        value = value.replace("\"", "\\\"")
        value = value.replace("'", "\\'")
        return "    <string name=\"{}\">{}</string>\n".format(key, value)