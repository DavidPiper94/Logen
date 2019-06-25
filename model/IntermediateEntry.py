class IntermediateEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.key == other.key and self.value == other.value

    def __str__(self):
        return "   IntermediateEntry: " + self.key + ": " + self.value