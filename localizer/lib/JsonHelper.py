import json
import os

def writeJSON(filepath, data):
    textFile = open(filepath, "w")
    json.dump(data, textFile, indent=4, ensure_ascii=False)

def readJSON(filepath):
    with open(filepath) as file:
        data = json.load(file)
        return data

def isJSONFile(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    return ext == ".json"

def dictToJSONString(dict):
    return json.dumps(dict)