
# Writes given content to given filepath.
def writeFile(filepath, content):
    textFile = open(filepath, "w")
    textFile.write(content)
    textFile.close()

def readFile(filepath):
    return open(filepath, "r").read()
