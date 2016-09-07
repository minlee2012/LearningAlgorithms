from Attribute import NominalAttribute
from Example import Example


class Examples(object):

    def __init__(self, *args, **kwargs):
        self.attributes = args
        self.exampleList = []

    def parse(self, inStream):
        newExample = Example(self.attributes)
        newExample.setAttributes(self.attributes)
        newList = inStream.split( )

        for index, item in enumerate(newList):
            if type(self.attributes.get(index)) == NominalAttribute:
                newExample.add(self.attributes.get(index).getIndex(item))
            else:
                newExample.add(item)
        self.exampleList.append(newExample)

    def getExamplesList(self):
        return self.exampleList

    def setAttributes(self, inAttributes):
        self.attributes = inAttributes

    def add(self, inExample):
        self.exampleList.append(inExample)

    def __str__(self):
        return "@examples\n" + "".join("\n".join(str(item) for item in self.exampleList))