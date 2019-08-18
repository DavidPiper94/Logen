from typing import List

from Logen.model.IntermediateEntry import IntermediateEntry
from Logen.model.IntermediateLocalization import IntermediateLocalization

class MergeResult():
    
    def __init__(self, result: IntermediateLocalization, missingEntries: List[IntermediateEntry]):
        self.result = result
        self.missingEntries = missingEntries

    def __eq__(self, other: object) -> bool:
        """Override the default Equals behavior"""
        if not isinstance(other, MergeResult): return NotImplemented

        sameResult = self.result == other.result
        sameMissingEntries = self.missingEntries == other.missingEntries
        return sameResult and sameMissingEntries 
    
    def __str__(self) -> str:
        description = "MergeResult of two IntermediateLoclaizations:\n" + str(self.result) + "\nMissing Entries:"
        for entry in self.missingEntries:
            description += "{}, ".format(entry)
        return description