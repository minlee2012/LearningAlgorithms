from Attribute import NominalAttribute


class Example(object):

    def __init__(self, *args, **kwargs):
        self.attributes = args
        self.values = []
        self.n = 0

    def add(self, value):
        self.values.append(value)

    def setAttributes(self, attributes):
        self.attributes = attributes

    def __str__(self):

        newList = []
        for index, item in enumerate(self.values):
            if type(self.attributes.get(index)) == NominalAttribute:
                newList.append(self.attributes.get(index).getValue(self.values[index]))
            else:
                newList.append(self.values[index])

        return " ".join(newList)
