class IntermediateLanguage: 

    def __init__(self, languageIdentifier, intermediateEntries):
        self.languageIdentifier = languageIdentifier
        self.intermediateEntries = intermediateEntries
        
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if not type(other) is IntermediateLanguage:
            return False
        
        sameIdentifier = self.languageIdentifier == other.languageIdentifier
        sameEntries = self.intermediateEntries.sort(key = lambda x: x.key) == other.intermediateEntries.sort(key = lambda x: x.key)
        return sameIdentifier and sameEntries

    def __str__(self):
        description = "IntermediateLanguage:\n   LanguageIdentifier: {}\n".format(self.languageIdentifier)
        for entry in self.intermediateEntries:
            description += str(entry) + "\n"
        return description