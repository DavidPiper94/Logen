from ConverterInterface import ConverterInterface as Base

class AndroidConverter(Base):

    def fileExtension(self): return ".xml"

    def toIntermediate(self, filepath):
        pass

    def fromIntermediate(self, intermediateLocalization):
        pass