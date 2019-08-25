import unittest
import pathlib
from typing import List

from ..converter.AndroidConverter import AndroidConverter
from ..converter.JSONConverter import JSONConverter
from ..converter.iOSConverter import iOSConverter
from ..lib import FileHelper
from ..model.IntermediateEntry import IntermediateEntry
from ..model.IntermediateLanguage import IntermediateLanguage
from ..model.IntermediateLocalization import IntermediateLocalization
from ..model.LocalizationFile import LocalizationFile

from ..tests import TestHelper

class Bigtests(unittest.TestCase):

    def test_vsCode(self):
        jsonFilepath = ".vscode/launch.json"
        jsonIntermediate = JSONConverter().toIntermediate(jsonFilepath)
        self.assertIsNone(jsonIntermediate)

    def test(self):
        bigtestPath = "./Logen/tests/bigtests"

        # Only execute tests if bigtests folder exists
        if not FileHelper.exists(bigtestPath):
            pass

        # Define all registers and extract processable extensions.
        converter = [iOSConverter(), AndroidConverter(), JSONConverter()]
        extensions = list(map(lambda x: x.fileExtension(), converter))

        # Find all files with an extension which can be processed by any converter.
        convertableFilepaths = self._findConvertableFilepaths(bigtestPath, extensions)
            
        # 1. alle mit gleicher extension finden
        # Sort files by filename and extension.
        # Structure will be { 'filename': { 'extension': [path, path, ...] } }
        sortedFilepathsDict = self._structureConvertableFilepaths(convertableFilepaths)

        # 2. alle mit entsprechender converter in intermediate umwandeln
        # 3. die mit gleicher extension mergen
        intermediateLocalizations = self._buildListOfIntermediateLocalizations(sortedFilepathsDict, converter)

        # 4. vergleichen
        for filename, listOfLocalizations in intermediateLocalizations.items():
            for localization in listOfLocalizations:
                # Assure all are the same by comparing all items to the first localization in the list.
                expectation = localization
                actual = listOfLocalizations[0]
                self.assertEqual(
                    expectation, 
                    actual, 
                    msg = TestHelper.errorMessageForIntermediateLocalization(expectation, actual) + "at file: {}".format(filename)
                )
                
    def _filenameFor(self, path):
        ext = FileHelper.fileExtension(path)
        return FileHelper.filename(path).replace(ext, '')

    def _findConvertableFilepaths(self, inDirectory: str, validExtension: List[str]) -> List[str]:
        convertableFilepaths = []
        for extension in validExtension:
            for path in pathlib.Path(inDirectory).rglob("*{}".format(extension)):
                convertableFilepaths.append(str(path))
        return convertableFilepaths

    def _structureConvertableFilepaths(self, convertableFilepaths: List[str]) -> List[str]:
        sortedFilepathsDict = {}
        for filepath in convertableFilepaths:
            filename = self._filenameFor(filepath)
            extension = FileHelper.fileExtension(filepath)

            if not filename in sortedFilepathsDict:
                # Add empty dict as starting point for this filename.
                sortedFilepathsDict[filename] = {}

            if not extension in sortedFilepathsDict[filename]:
                # Add empty list as starting point for this extension.
                sortedFilepathsDict[filename][extension] = []

            sortedFilepathsDict[filename][extension].append(filepath)
        return sortedFilepathsDict

    def _buildListOfIntermediateLocalizations(self, structuredConvertableFilepahts: List[str], converter) -> dict:        
        intermediateLocalizations = {}
        for filename, extensionDict in structuredConvertableFilepahts.items():
            for extension, pathList in extensionDict.items():

                # Get first converter available for current extension.
                currentConverter = list(filter(lambda x: x.fileExtension() == extension, converter))[0]
                # Start with an empty intermediateLocalization. All resulting intermediates will be merged into this one.
                intermediateWithSameExtension = None

                for path in pathList:
                    newIntermediate = currentConverter.toIntermediate(path)

                    if intermediateWithSameExtension is None:
                        intermediateWithSameExtension = newIntermediate
                    else:
                        merged = currentConverter.merge(intermediateWithSameExtension, newIntermediate)
                        if merged is not None:
                            intermediateWithSameExtension = merged.result
                            self.assertEqual(
                                [],
                                merged.missingEntries,
                                msg = self._mergedErrorMessage(path, merged)
                            )
                        else:
                            # This is the case for .vscode/settings.json
                            pass
                
                if not filename in intermediateLocalizations:
                    intermediateLocalizations[filename] = []

                intermediateLocalizations[filename].append(intermediateWithSameExtension)
        return intermediateLocalizations

    def _mergedErrorMessage(self, path: str, merged) -> str:
        msg = "\n-----"
        msg += "\nDetails:"
        msg += "\n-----"
        msg += "\nError at path: {}".format(path)
        msg += "\nDifference:"
        msg += "\n{}".format(str(merged))
        return msg

if __name__ == '__main__':
    unittest.main()
