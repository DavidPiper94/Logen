class IntermediateLocalization:

    def __init__(self, localizationIdentifier, intermediateLanguages):
        self.localizationIdentifier = localizationIdentifier
        self.intermediateLanguages = intermediateLanguages

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.localizationIdentifier == other.localizationIdentifier and self.intermediateLanguages == other.intermediateLanguages

    def __str__(self):
        description = "IntermediateLocalization:\nLocalizationIdentifier: {}\n".format(self.localizationIdentifier)
        for language in self.intermediateLanguages:
            description += str(language)
        return description