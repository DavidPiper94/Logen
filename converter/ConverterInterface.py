import abc

class ConverterInterface:

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def fileExtension(self): raise NotImplementedError

    @abc.abstractmethod
    def toIntermediate(self, filepath): raise NotImplementedError

    @abc.abstractmethod
    def fromIntermediate(self, intermediateLocalization): raise NotImplementedError