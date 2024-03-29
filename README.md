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

- More localizations to support even more languages and platforms (e.g. for Python).
- Make it possible to register external converter.
- Add functionallity to validate existing localizations both syntactically as well as content wise.

# More information

[An intro to Logen](https://medium.com/@HeyDaveTheDev/logen-converting-localization-formats-f32fcfeca95d)</br>
[An overview of the converting process](https://medium.com/@HeyDaveTheDev/an-overview-of-converting-localization-formats-with-logen-2bc6606d6bb0)</br>
[A deepdive into the project](https://medium.com/@HeyDaveTheDev/logen-a-deep-dive-into-the-project-fbbc1a816e15)</br>
[Adding your own converter](https://medium.com/@HeyDaveTheDev/logen-adding-your-own-converter-179b45c63e0e)

# License

MIT
