class MergeResult():
    
    def __init__(self, result, missingEntries):
        self.result = result
        self.missingEntries = missingEntries

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.result == other.result and self.missingEntries == other.missingEntries
    
    def __str__(self):
        description = "MergeResult of two IntermediateLoclaizations:\n" + str(self.result) + "\nMissing Entries:"
        for entry in self.missingEntries:
            description += "{}, ".format(entry)
        return description