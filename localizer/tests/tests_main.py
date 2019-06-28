import unittest

from localizer import main

class MainTests(unittest.TestCase):

    def test_selectImporterForFileExtension(self):
        importer = main.selectImporterForFileExtension(".json")
        self.assertEquals(importer.fileExtension(), ".json")

    def test_outputConverterForFileExtension(self):
        outputConverter = main.outputConverterForFileExtension(".nope")
        self.assertEquals(len(outputConverter), len(main.registeredConverter()))

if __name__ == '__main__':
    unittest.main()