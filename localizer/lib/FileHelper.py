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
    return open(filepath, "r").read()

def readLines(filepath):
    return open(filepath).read().split("\n")

def fileExtension(filepath):
    return os.path.splitext(filepath)[-1].lower()

#--------------------
# Direcories
#--------------------

def exists(filepath):
    return os.path.exists(filepath)

def createDir(filepath):
    os.makedirs(filepath)

def removeDir(filepath):
    shutil.rmtree(path)