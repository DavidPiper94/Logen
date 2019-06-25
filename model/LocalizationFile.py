class LocalizationFile:

    def __init__(self, filepath, filecontent):
        self.filepath = filepath
        self.filecontent = filecontent

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.filepath == other.filepath and self.filecontent == other.filecontent

    def __str__(self):
         return "LocalizationFile:\nFilepath: {}\nContent: {}".format(self.filepath, self.filecontent)
