def start(args, converter):
    print("Available converter:\n")
    descriptions = list(map(lambda x: describe(x), converter))
    for description in descriptions:
        print(description)

def describe(converter):
    content = "Identifier: {}\n".format(converter.identifier()) 
    content += "file extension: {}\n".format(converter.fileExtension())
    content += "import description: {}\n".format(converter.importDescription())
    content += "export description: {}\n".format(converter.exportDescription())
    return content