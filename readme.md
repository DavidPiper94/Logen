This pyhton script generates the localization for an iOS and an Android project. It takes following arguments which have to be provided in the correct order:

1) Path to source directory. This directory has to contain only json files.
2) Path to destination directory. Into this directory a new directory will be added which contains the generated files.

Additionally you can add following flags:
-h or --help: Shows this text as help.
-m or --mock: Präfixes all strings with {}. This can be used to check if all texts are localized.
-l or --long: Präfixes all strings with the first 300 chars of 'Lorem ipsum' to test long strings.