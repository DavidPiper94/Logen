from localizer.model.IntermediateLocalization import IntermediateLocalization

class MergeResult():
    
    def __init__(self, result: IntermediateLocalization, missingEntries: list):
        self.result = result
        self.missingEntries = missingEntries

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if not type(other) is MergeResult:
            return False

        sameResult = self.result == other.result
        sameMissingEntries = self.missingEntries == other.missingEntries
        return sameResult and sameMissingEntries 
    
    def __str__(self):
        description = "MergeResult of two IntermediateLoclaizations:\n" + str(self.result) + "\nMissing Entries:"
        for entry in self.missingEntries:
            description += "{}, ".format(entry)
        return description