import argparse
import sys

from localizer.converter.AndroidConverter import AndroidConverter
from localizer.converter.JSONConverter import JSONConverter
from localizer.converter.iOSConverter import iOSConverter

from localizer import main_subcommand_convert
from localizer import main_subcommand_list

#--------------------
# variables
#--------------------

registeredConverter = [
        iOSConverter(),
        AndroidConverter(),
        JSONConverter()
]

#--------------------
# Setup CLI
#--------------------

def setupParser():
    parser = argparse.ArgumentParser(description = "Description")
    subparsers = parser.add_subparsers(help = "Subparser")

    parser_convert = subparsers.add_parser("convert", help = "Lists all available converter.")
    parser_convert.add_argument("source", help = "Path to source file")
    parser_convert.add_argument("destination", help = "Path at which destination directory will be created")
    parser_convert.add_argument("importConverter", help = "Identifier of the converter to be used to import content of the given file.")
    parser_convert.add_argument("exportConverter", help = "Identifier of the converter to be used to export content with a specific format.")
    parser_convert.add_argument("-d", "--dryRun", action = "store_true", help = "If true, result will be printed to the console and not saved.")
    parser_convert.add_argument("-v", "--verbose", action = "store_true", help = "If true, additional information will be written to the console.")
    parser_convert.set_defaults(func = subcommandConvert)

    parser_list = subparsers.add_parser("list", help = "Lists all available converter.")
    parser_list.set_defaults(func = subcommandList)

    return parser

def subcommandList(args):
    main_subcommand_list.start(args, registeredConverter)

def subcommandConvert(args):
    main_subcommand_convert.start(args, registeredConverter)

#--------------------
# Main
#--------------------

if __name__ == "__main__":
    parser = setupParser()
    args = parser.parse_args()
    args.func(args)
    
