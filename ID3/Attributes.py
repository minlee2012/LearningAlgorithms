from Attribute import Attribute
from Attribute import NumericAttribute
from Attribute import NominalAttribute

class Attributes(object):

    def __init__(self):
        self.attributes = []
        self.hasNumericAttributes = False
        self.hasNominalAttributes = False
        self.classIndex = -1 #for us, always the last attribute in the file (the attribute we're trying to predict)

    def add(self, Attribute):
        self.attributes.append(Attribute)
        if type(Attribute) == NumericAttribute:
            self.hasNumericAttributes = True
        elif type(Attribute) == NominalAttribute:
            self.hasNominalAttributes = True

    def getClassIndex(self):
        return self.classIndex

    def getAttributesList(self):
        return self.attributes

    def getHasNominalAttributes(self):
        return self.hasNominalAttributes

    def getHasNumericAttributes(self):
        return self.hasNumericAttributes

    def get(self, i):
        return self.attributes[i]

    def getClassAttribute(self):
        return self.attributes[self.classIndex]

    def getIndex(self, name):
        for index, item in enumerate(self.attributes):
            if item == name:
                return index
            else:
                return "Value not found in Attributes"

    def getSize(self):
        return len(self.attributes)

    def parse(self, inStream):
        newStream = inStream.split( )
        newAttribute = Attribute.factory(newStream[2])
        newAttribute.setName(newStream[1])

        for num in range(2, len(newStream)):
            if type(newAttribute) == NominalAttribute:
                newAttribute.addValue(newStream[num])
            else:
                pass
        self.add(newAttribute)
        self.setClassIndex(self.getSize()-1)

    def setClassIndex(self, cI):
        self.classIndex = cI

    def __str__(self):
        return "".join("\n".join(str(self.attributes[num]) for num in range(0, len(self.attributes))))