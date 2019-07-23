import sys

from localizer.lib import FileHelper
from localizer.lib import TerminalStyle

#--------------------
# properties
#--------------------

sourceFilepath = ""
destinationDirectory = ""
importConverterIdentifier = ""
exportConverterIdentifier = ""
dryRun = False

#--------------------
# Starting point
#--------------------

def start(args, converter):
    _parseArgsForConverting(args, converter)
    intermediate = _importToIntermediateLocalization(sourceFilepath, converter)
    _exportToLocalizationFile(intermediate, converter)

#--------------------
# private helper
#--------------------

def _parseArgsForConverting(args, converter):

    # select and validate converter for export
    global exportConverterIdentifier
    exportConverterIdentifier = args.exportConverter
    selectedExportConverter = list(filter(lambda x: x.identifier() == exportConverterIdentifier, converter))
    if len(selectedExportConverter) == 0:
        _handleError("ERROR: Converter with identifier {} not found".format(exportConverterIdentifier))

    # validate source filepath
    global sourceFilepath
    sourceFilepath = args.source
    if not FileHelper.exists(sourceFilepath):
        _handleError("ERROR: Source does not exists")
        
    # select and validate converter for import
    global importConverterIdentifier
    importConverterIdentifier = args.importConverter
    extension = FileHelper.fileExtension(sourceFilepath)
    # TODO: Better comparison, e.g. lowercased
    matchingImportConverter = list(filter(lambda x: x.fileExtension() == extension and x.identifier() == importConverterIdentifier, converter))
    if len(matchingImportConverter) == 0:
        _handleError("ERROR: No matching converter found with identifier {} for fileextension {}".format(importConverterIdentifier, extension))
    else:
        importConverterIdentifier = matchingImportConverter[0].identifier()
    
    # save and handle dryRun argument
    global dryRun
    dryRun = args.dryRun
    if dryRun:
        if args.verbose:
            _printSummary(sourceFilepath, "dryRun", importConverterIdentifier, exportConverterIdentifier)
        # If dryRun is enabled, there is no need to process destination directory.
        return

    # save and validate destination filepath
    global destinationDirectory
    destinationDirectory = args.destination
    if not FileHelper.exists(destinationDirectory):
        FileHelper.createDir(destinationDirectory)
    else:
        _handleWarning("WARNING: Destination directory already exists. Do you want to override it?")
        # TODO: Ask
        #FileHelper.removeDir(destinationDirectory)
        #FileHelper.createDir(destinationDirectory)
    
    # At this point everything was validated and nothing can go wrong (hopefully).
    if args.verbose:
        _printSummary(sourceFilepath, destinationDirectory, importConverterIdentifier, exportConverterIdentifier)

def _importToIntermediateLocalization(sourceFilepath, converter):
    importer = list(filter(lambda x: x.identifier() == importConverterIdentifier, converter))
    return importer[0].toIntermediate(sourceFilepath)

def _exportToLocalizationFile(intermediateLocalization, converter):
    exportConverter = list(filter(lambda x: x.identifier() == exportConverterIdentifier, converter))
    for exporter in exportConverter:
        for file in exporter.fromIntermediate(intermediateLocalization):
            _handleLocalizationFile(file)

def _handleLocalizationFile(localizationFile):
    global dryRun
    if dryRun:
        print(localizationFile.filecontent)
    else:
        destination = destinationDirectory + "/" + localizationFile.filepath
        _writeFile(destination, localizationFile.filecontent)

def _writeFile(path, content):
    directoryPath = FileHelper.directoryPath(path)

    if FileHelper.exists(path):
        pass

    else:
        FileHelper.createDir(directoryPath)
        FileHelper.writeFile(path, content)

#--------------------
# cli output
#--------------------

def _printSummary(sourceFilepath, destinationFilepath, importConverterIdentifier, exportConverterIdentifier):
    _handleInfo(
        "Summary:\n"
        + "input: {}\n".format(sourceFilepath)
        + "destination: {}\n".format(destinationFilepath)
        + "converter for import: {}\n".format(importConverterIdentifier)
        + "converter for export: {}".format(exportConverterIdentifier)
    )

def _handleError(errorText):
    print(TerminalStyle.FAIL + errorText + TerminalStyle.ENDC)
    sys.exit()

def _handleWarning(warningText):
    print(TerminalStyle.WARNING + warningText + TerminalStyle.ENDC)

def _handleInfo(infoText):
    print(TerminalStyle.GREEN + infoText + TerminalStyle.ENDC)
