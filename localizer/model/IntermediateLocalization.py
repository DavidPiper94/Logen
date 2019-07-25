class IntermediateLocalization:

    def __init__(self, localizationIdentifier, intermediateLanguages):
        self.localizationIdentifier = localizationIdentifier
        self.intermediateLanguages = intermediateLanguages

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if not type(other) is IntermediateLocalization:
            return False

        sameIdentifier = self.localizationIdentifier == other.localizationIdentifier
        sameLanguages = sorted(self.intermediateLanguages, key = lambda x: x.languageIdentifier) == sorted(other.intermediateLanguages, key = lambda x: x.languageIdentifier)
        return sameIdentifier and sameLanguages

    def __str__(self):
        description = "IntermediateLocalization:\nLocalizationIdentifier: {}\n".format(self.localizationIdentifier)
        for language in self.intermediateLanguages:
            description += str(language)
        return description