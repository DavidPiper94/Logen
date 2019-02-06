import json

def writeJSON(filepath, data):
    textFile = open(filepath, "w")
    json.dump(data, textFile, indent=4, ensure_ascii=False)

def readJSON(filepath):
    with open(filepath) as file:
        data = json.load(file)
        return data
