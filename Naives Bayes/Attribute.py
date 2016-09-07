class Attribute(object):

    def __init__(self, *args):
        self.name = args
        self.size = 0

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getSize(self):
        return 0

    def __print__(self):
        print self.name

    #factory function: creates Numeric or Nominal Attribute depending on type
    def factory(type):

        if type == "numeric" or type == "Numeric":
            return NumericAttribute()
        else:
            return NominalAttribute()
    factory = staticmethod(factory)


class NumericAttribute(Attribute):

    def __init__(self, *args):
        super(NumericAttribute, self).__init__(*args)
        if(len(args) > 0):
            self.name = args[0]
        self.size = 0

    def getSize(self):
        return self.size

    def __str__(self):
        return "@attribute " + str(self.name) + " numeric"


class NominalAttribute(Attribute):

    def __init__(self, *args):
        super(NominalAttribute, self).__init__(*args)
        if(len(args) > 0):
            self.name = args[0]
        self.size = 0
        self.domain = []

    def addValue(self, value):
        self.domain.append(value)
        self.size += 1

    def getIndex(self, value):
        for index, item in enumerate(self.domain):
            if item == value:
                return index
        else:
            return "Value not found in Nominal Attribute"

    def getSize(self):
        return len(self.domain)

    def getValue(self, index):
        return self.domain[index]

    def __str__(self):
        return "@attribute " + str(self.name) + " " + " ".join(self.domain)