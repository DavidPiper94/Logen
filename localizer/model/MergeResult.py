class MergeResult():
    
    def __init__(self, mergedIntermediateLocalization, listOfMissingEntries):
        self.mergedIntermediateLocalization = mergedIntermediateLocalization
        self.listOfMissingEntries = listOfMissingEntries

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.mergedIntermediateLocalization == other.mergedIntermediateLocalization and self.listOfMissingEntries == other.listOfMissingEntries
    
    def __str__(self):
        description = "MergeResult of two IntermediateLoclaizations:\n" + str(self.mergedIntermediateLocalization) + "\nMissing Entries:"
        for entry in self.listOfMissingEntries:
            description += "{}, ".format(entry)
        return description