This pyhton script generates the localization for an iOS and an Android project. It takes following arguments which have to be provided in the correct order:

1) Path to source directory. This directory has to contain only json files.
2) Path to destination directory. Into this directory a new directory will be added which contains the generated files.

Additionally you can add following flags:
-h or --help: Shows this text as help.
-m or --mock: Präfixes all strings with {}. This can be used to check if all texts are localized.
-l or --long: Präfixes all strings with the first 300 chars of 'Lorem ipsum' to test long strings.

This project brings it's own python environment with pipenv.
For more information to pipenv see: https://github.com/pypa/pipenv and https://pipenv.readthedocs.io/en/latest/

How to use:
* *git clone [reponame]*: Clones this repository.
* *cd [foldername]*: Enters this directory.
* *pipenv shell*: Starts a new python environment.
* *pipenv install*: Downloads and installs all needed dependencies into the new environment.
* *python main.py path/to/source/directory path/to/destination/directory*: Executes the script.
* *exit*: Ends and leaves new environment.