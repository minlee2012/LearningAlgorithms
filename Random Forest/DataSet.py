import random
from Example import Example
from Examples import Examples
from Attribute import Attribute
from Attributes import Attributes
from math import log


class DataSet(object):

    def __init__(self, *args):
        self.name = ""
        self.attributes = Attributes()
        self.examples = Examples()
        self.examples.setAttributes(self.attributes)
        self.seed = 2026875034
        self.setOptions(args)

    def add(self, input):
        if type(input) == DataSet:
            for items in input.getAttributes().getAttributesList():
                self.attributes.add(items)
            for items in input.getExamples().getExamplesList():
                self.examples.add(items)
        elif type(input) == Example:
            self.examples.add(input)

    def getAttributes(self):
        return self.attributes

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.attributes.setClassIndex(attributes.getClassIndex())

    def getExamples(self):
        return self.examples

    def getHasNominalAttributes(self):
        self.attributes.getHasNominalAttributes()

    def getHasNumericAttributes(self):
        self.attributes.getHasNumericAttributes()

    def load(self, filename):
        with open(filename, "r") as inputFile:
            self.parse(inputFile)

    def parse(self, inStream):
        for line in inStream:
                if "@dataset" in line:
                    tempStream = line.split()
                    self.name = tempStream[1]
                elif "@attribute" in line:
                    self.attributes.parse(line)
                elif "@examples" in line:
                    for line in inStream:
                        if line == "\n":
                            pass
                        else:
                            self.examples.parse(line)

    def setOptions(self, arguments):
        for num in range(0, len(arguments)):
            if arguments[num] == "-s":
                self.setSeed(random.seed(arguments[num+1]))
                break

    def getSeed(self):
        return self.seed

    def setSeed(self, inSeed):
        self.seed = inSeed

    def getBestSplit(self):
        bestSplitIndex = -1
        maxGain = 0
        for item in range(0, len(self.attributes.attributes) - 1):
            if self.gain(item) > maxGain:
                maxGain = self.gain(item)
                bestSplitIndex = item
        return bestSplitIndex

    def splitOnAttribute(self, attributeIndex):
        childrenDataSets = []
        for item in range(0, len(self.attributes.attributes[attributeIndex].domain)):
            childrenDataSets.append(DataSet())
            childrenDataSets[item].setAttributes(self.attributes)
        for items in self.examples.getExamplesList():
            childrenDataSets[items.values[attributeIndex]].add(items)
        return childrenDataSets

    def entropy(self):
        counts = self.counter()
        entropy = 0.0
        for item in counts.values():
            if float(item/float(len(self.examples.getExamplesList()))) == 0.0:
                pass
            else:
                entropy += (-item/float(len(self.examples.getExamplesList())))*log((item/float(len(self.examples.getExamplesList()))),2)
        return round(entropy,2)

    def gain(self, attributeIndex):
        gain = 0
        start = self.entropy()
        summation = 0
        for items in self.splitOnAttribute(attributeIndex):
            summation += (float(len(items.examples.getExamplesList()))/len(self.examples.getExamplesList())) * items.entropy()
        gain = start - summation
        return round(gain,2)

    def majority(self):
        counts = self.counter()
        return max(counts, key = counts.get)

    def counter(self):
        counts = {}
        for item in self.examples.getExamplesList():
            if self.attributes.attributes[self.attributes.classIndex].domain[item.values[self.attributes.classIndex]] in counts.keys():
                counts[self.attributes.attributes[self.attributes.classIndex].domain[item.values[self.attributes.classIndex]]] += 1
            else:
                counts[self.attributes.attributes[self.attributes.classIndex].domain[item.values[self.attributes.classIndex]]] = 1
        return counts

    def nominalToBinary(self):
        newDataSet = DataSet()
        newAttributes = Attributes()
        for items in self.attributes.attributes:
            if len(items.domain) > 2:
                binaryDomain = bin(len(items.domain))
                for index, char in enumerate(str(binaryDomain)):
                    if index >= len(str(binaryDomain))-2:
                        pass
                    else:
                        newAttribute = Attribute.factory("nominal")
                        newAttribute.setName(items.name + str(index))
                        newAttribute.addValue(str(0))
                        newAttribute.addValue(str(1))
                        newAttributes.add(newAttribute)
            else:
                newAttributes.add(items)
        newDataSet.setAttributes(newAttributes)
        newDataSet.attributes.setClassIndex(len(newAttributes.attributes)-1)
        #ADJUST EXAMPLES NEXT
        return newDataSet

    def __str__(self):
        return "@dataset " + self.name + "\n" + str(self.attributes) + "\n\n" + str(self.examples)