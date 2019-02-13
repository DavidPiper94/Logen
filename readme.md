Generates localization files for iOS and Android projects.

# Setup

This project brings it's own python environment with pipenv.
For more information to pipenv see: https://github.com/pypa/pipenv and https://pipenv.readthedocs.io/en/latest/

* *git clone [reponame]*: Clones this repository.
* *cd [foldername]*: Enters this directory.
* *pipenv shell*: Starts a new python environment.
* *pipenv install*: Downloads and installs all needed dependencies into the new environment.
* *exit*: Ends and leaves new environment.

# How to use

positional arguments:
  * source:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Path to source directory
  * destination:  Path at which destination directory will be created

optional arguments:
  * -h, --help: &nbsp;&nbsp; Show this help message and exit
  * -m, --mock: Präfixes all strings with the content of templates/template_common_mock. This can be used to check if all texts are localized.
  * -l, --long: &nbsp;&nbsp;&nbsp; Präfixes all strings with the first 300 chars of 'Lorem ipsum' to test long strings.
