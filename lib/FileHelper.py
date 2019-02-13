import os

# Writes given content to given filepath.
def writeFile(filepath, content):
    textFile = open(filepath, "w")
    textFile.write(content)
    textFile.close()

def readFile(filepath):
    return open(filepath, "r").read()

def readLines(filepath):
    return open(filepath).read().split("\n")

def fileExtension(filepath):
    return os.path.splitext(filepath)[-1].lower()