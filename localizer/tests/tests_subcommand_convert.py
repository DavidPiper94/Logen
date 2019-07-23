import unittest

from localizer.tests.ConverterSpy import ConverterSpy
from localizer import main_subcommand_convert
from localizer import main

class SubcommandConvertTests(unittest.TestCase):

    spy = ConverterSpy()

    # def test_parseArgsForConverting(self):
    #     self.spy.changeFileExtensionTo("json")
    #     self.spy.changeIdentifierTo("spy")
    #     testArgs = [
    #         "convert", 
    #         "localizer/tests/bigtests/localization_Src/information.json", 
    #         "/", 
    #         "spy",
    #         "spy",
    #         "--dryRun",
    #         "--verbose"
    #     ]
    #     parsedTestArgs = main.parse(testArgs)
    #     main_subcommand_convert._parseArgsForConverting(parsedTestArgs, [self.spy])
    
    def test_importToIntermediateLocalization(self):
        """Assures that given a converter with correct identifier, the converter is used correctly."""
        
        # prepare sut
        main_subcommand_convert.importConverterIdentifier = "spy"

        # setup spy
        self.spy.changeIdentifierTo("spy")

        # define test parameter
        testSourcePath = ""
        converter = [self.spy]

        # execute and validate
        main_subcommand_convert._importToIntermediateLocalization(testSourcePath, converter)        
        self.assertTrue(self.spy.didImport)

if __name__ == '__main__':
    unittest.main()