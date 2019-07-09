class IntermediateLanguage: 

    def __init__(self, languageIdentifier, intermediateEntries):
        self.languageIdentifier = languageIdentifier
        self.intermediateEntries = intermediateEntries
        
    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.languageIdentifier == other.languageIdentifier and self.intermediateEntries.sort(key = lambda x: x.key) == other.intermediateEntries.sort(key = lambda x: x.key)

    def __str__(self):
        description = "IntermediateLanguage:\n   LanguageIdentifier: {}\n".format(self.languageIdentifier)
        for entry in self.intermediateEntries:
            description += str(entry) + "\n"
        return description