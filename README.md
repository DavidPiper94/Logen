# Logen

Logen generates localization files in various formats and can converte one format to another.

- Generate localization files for iOS and Android
- Convert localization files from iOS to Android or the other way around
- Easily add new converter for any localization format you need!

Logen provides a foundation for adding even more converter if you want to generate a localization format which is currently not supported.

# How to install

Installing Logen is as easy as ```pip install Logen```

# How to use

Possible subcommands are *convert* and *list*. 

### Convert

Converts one localization format to another.

Positional arguments: 
- filepath to source file
- filepath to destination directory
- identifier of converter to import
- identifier of converter to export

Optional arguments:
- -f/--force for overwriting existing destination directories
- -d/--dryRun for printing result to console instead of writing to a file
- -v/--verbose for additional information

### List

Lists all available converter and their descriptions.

# Planned features

- Adding guides on how to use it and how to add a new custom converter.
- More localizations to support even more languages and platforms (e.g. for Python).
- Make it possible to register external converter.
- Add functionallity to validate existing localizations both syntactically as well as content wise.

# More information

[An intro to Logen](https://medium.com/@HeyDaveTheDev/logen-converting-localization-formats-f32fcfeca95d)</br>
WIP:  An overview of the converting process</br>
TODO: A deepdive into the project</br>
TODO: Adding support for a new format

# License

MIT
