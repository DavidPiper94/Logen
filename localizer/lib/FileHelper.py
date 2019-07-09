import os
import shutil

#--------------------
# Files
#--------------------

def writeFile(filepath, content):
    textFile = open(filepath, "w")
    textFile.write(content)
    textFile.close()

def readFile(filepath):
    textFile = open(filepath, "r")
    content = textFile.read()
    textFile.close()
    return content

def readLines(filepath):
    return readFile(filepath).split("\n")

def filename(filepath):
    return os.path.basename(filepath)

def directoryName(filepath):
    return os.path.dirname(filepath).split('/')[-1]

def directoryPath(filepath):
    return os.path.dirname(filepath)

def fileExtension(filepath):
    return os.path.splitext(filepath)[-1].lower()

def exists(filepath):
    return os.path.exists(filepath)

#--------------------
# Direcories
#--------------------

def createDir(filepath):
    os.makedirs(filepath)

def removeDir(filepath):
    shutil.rmtree(path)