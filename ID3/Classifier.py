from DataSet import DataSet
from Example import Example
from Performance import Performance

class Classifier(object):

    def __init__(self, *args):
        pass

    def train(self, inDataSet):
        self.train = inDataSet

    def classify(self, inData):
        if type(inData) == Example:
            pass
        elif type(inData) == DataSet:
            pass
        else:
            print "Error in Classifier classify"

class knn(Classifier):

    def __init__(self, *args):
        super(knn, self).__init__(*args)
        self.k = 3
        self.instances = DataSet()
        self.setOptions(args)

    def train(self, inDataSet):
        self.instances = inDataSet

    def classify(self, input):
        neighbors = []
        if type(input) == Example:

            for index, item in enumerate(self.instances.getExamples().getExamplesList()):
                if len(neighbors) < self.k:
                    tempNeighbor = neighbor()
                    tempNeighbor.setNeighbor(self.instances.getAttributes().getAttributesList()[self.instances.getAttributes().getClassIndex()].domain[item.values[self.instances.getAttributes().getClassIndex()]], self.distance(input, item))
                    neighbors.append(tempNeighbor)
                else:
                    highestDist = -1
                    highestIndex = -1
                    for num in range(0, len(neighbors)):
                        if num < len(neighbors)-1:
                            if neighbors[num].distance >= neighbors[num + 1].distance:
                                highestDist = neighbors[num].distance
                                highestIndex = num
                            else:
                                highestDist = neighbors[num + 1].distance
                                highestIndex = num + 1
                        elif neighbors[num] < highestDist:
                            highestDist = neighbors[num]
                            highestIndex = num
                    if self.distance(input, self.instances.getExamples().getExamplesList()[index]) < highestDist:
                        newNeighbor = neighbor()
                        newNeighbor.setNeighbor(self.instances.getAttributes().getAttributesList()[self.instances.getAttributes().getClassIndex()].domain[item.values[self.instances.getAttributes().getClassIndex()]], self.distance(input,item))
                        neighbors[highestIndex] = newNeighbor

            return self.vote(neighbors)

        elif type(input) == DataSet:
            rightCount = 0
            for index, item in enumerate(self.instances.getExamples().getExamplesList()):
               if self.classify(self.instances.getExamples().getExamplesList()[index]) == self.instances.getAttributes().getClassAttribute().domain[self.instances.getExamples().getExamplesList()[index].values[self.instances.getExamples().attributes.getClassIndex()]]:
                    rightCount += 1
            performance = Performance()
            performance.setPerf(rightCount, len(self.instances.getExamples().getExamplesList()))
            return performance

    def setOptions(self, arguments):
        for num in range(0, len(arguments[0])):
            if arguments[0][num] == "-k":
                self.k = int(arguments[0][num+1])
            elif arguments[0][num] == "-t":
                newDataSet = DataSet()
                newDataSet.load(arguments[0][num+1])
                self.instances = newDataSet

    def distance(self, observation, example):
        total = 0
        for num in range(0, len(observation.attributes.getAttributesList())-1):
            if observation.values[num] != example.values[num]:
                total += 1
        return total

    def vote(self, neighbors):
        voteDict = {}
        for index, items in enumerate(neighbors):
            if items.classifier in voteDict.keys():
                voteDict[items.classifier] += 1
            else:
                voteDict[items.classifier] = 1
        return max(voteDict, key = voteDict.get)

class NaiveBayes(Classifier):

    def __init__(self, *args):
        super(NaiveBayes, self).__init__(*args)
        self.totalNumber = 0
        self.probabilities = [] #list of lists of probabilities
        self.setOptions(args)

    def train(self, inDataSet):
        for num in range(0, len(inDataSet.getAttributes().getAttributesList())):
            newList = []
            self.probabilities.append(newList)
        for items in inDataSet.getExamples().getExamplesList():
            for index, values in enumerate(items.values):
                if len(self.probabilities) == 0:
                    newProbability = probability()
                    newProbability.setFactors(inDataSet.getAttributes().getAttributesList()[index].domain[values], inDataSet.getAttributes().getAttributesList()[items.attributes.getClassIndex()].domain[items.values[items.attributes.getClassIndex()]])
                    newProbability.addValue()
                    self.probabilities[index].append(newProbability)
                else:
                    found = False
                    for probs in self.probabilities[index]:
                        if probs.attribute == inDataSet.getAttributes().getAttributesList()[index].domain[values] and probs.classifier == inDataSet.getAttributes().getAttributesList()[items.attributes.getClassIndex()].domain[items.values[items.attributes.getClassIndex()]]:
                            probs.addValue()
                            found = True
                    if not found:
                        newProbability = probability()
                        newProbability.setFactors(inDataSet.getAttributes().getAttributesList()[index].domain[values], inDataSet.getAttributes().getAttributesList()[items.attributes.getClassIndex()].domain[items.values[items.attributes.getClassIndex()]])
                        newProbability.addValue()
                        self.probabilities[index].append(newProbability)
        self.totalNumber = len(inDataSet.getExamples().getExamplesList())

    def classify(self, input):
        if type(input) == Example:
            prior = 1.0
            tempProbability = 1.0
            possibilities = {}
            for values in input.attributes.getAttributesList()[input.attributes.getClassIndex()].domain:
                for index,items in enumerate(input.values):
                    for probability in self.probabilities:
                        for index2, item in enumerate(probability):
                            if item.classifier == values and item.attribute == input.attributes.getAttributesList()[index].domain[items]:
                                tempProbability *= float(float(item.numExamples)/float(len(self.probabilities[index]) + len(input.attributes.getAttributesList()[index].domain)))
                for probability in self.probabilities[input.attributes.getClassIndex()]:
                    if probability.attribute == values:
                        prior = float(float(probability.numExamples)/float(self.totalNumber))
                possibilities[values] = (prior * tempProbability)
            return max(possibilities, key = possibilities.get)

        elif type(input) == DataSet:
            rightCount = 0
            count = 0
            possibilities = {}
            for values in input.getAttributes().getAttributesList()[input.getAttributes().getClassIndex()].domain:
                prior = 0.0
                tempProbability = 1.0
                for index, items in enumerate(input.getExamples().getExamplesList()):
                    for index2, item in enumerate(items.values):
                        for probability in self.probabilities[index2]:
                            if probability.classifier == values and probability.attribute == input.getAttributes().getAttributesList()[index2].domain[item]:
                                tempProbability *= float(float(probability.numExamples)/float(len(self.probabilities[index2]) + len(input.getAttributes().getAttributesList()[index2].domain)))
                    for probability in self.probabilities[input.getAttributes().getClassIndex()]:
                        if probability.attribute == values:
                            prior = float(float(probability.numExamples)/float(len(input.getExamples().getExamplesList())))
                    possibilities[values] = (prior * tempProbability)
                    if max(possibilities, key = possibilities.get) == input.getAttributes().getAttributesList()[input.getAttributes().getClassIndex()].domain[items.values[input.getAttributes().getClassIndex()]]:
                        rightCount += 1
                    count += 1
            performance = Performance()
            performance.setPerf(rightCount, count)
            return performance

    def setOptions(self, arguments):
        for num in range(0, len(arguments[0])):
            if arguments[0][num] == "-t":
                newDataSet = DataSet()
                newDataSet.load(arguments[0][num+1])
                self.train(newDataSet)

class neighbor(object):

    def __init__(self):
        self.classifier = ""
        self.distance = -1

    def setNeighbor(self, attribute, distance):
        self.classifier = attribute
        self.distance = distance

    def __str__(self):
        return str(self.classifier) + " " + str(self.distance)

class probability(object):

    def __init__(self):
        self.attribute = ""
        self.classifier = ""
        self.numExamples = 1.0 #start at one for additive smoothing
        self.prior = False

    def addValue(self):
        self.numExamples += 1

    def setFactors(self, attribute, classifier):
        self.attribute = attribute
        self.classifier = classifier
        if attribute == classifier:
            self.prior = True

    def __str__(self):
        return "(" + str(self.attribute) + "|" + str(self.classifier) + "): " + str(round(float(self.numExamples),2))

class ID3(Classifier):
    def __init__(self, *args):
        super(ID3, self).__init__(*args)
        self.root = Node()

    def train(self, inDataSet):
        initCount = inDataSet.counter()
        if len(initCount) < 2: #if homogenous
            self.root.label = max(initCount, key = initCount.get)
        else:
            self.root.attribute = inDataSet.getBestSplit()
            childrenData = inDataSet.splitOnAttribute(self.root.attribute)
            for num in range(0, len(childrenData)):
                self.root.children.append(ID3())
                if len(childrenData[num].examples.getExamplesList()) == 0: #if empty node
                    self.root.children[num].label = inDataSet.majority()
                else:
                    self.root.children[num].train(childrenData[num])
        return self

    def classify(self, inData):
        rightCount = 0
        for items in inData.examples.getExamplesList():
            currentNode = self.root
            while currentNode.attribute > 0:
                currentNode = currentNode.children[items.values[currentNode.attribute]].root
            if items.attributes.attributes[items.attributes.getClassIndex()].getIndex(currentNode.label) == items.values[items.attributes.getClassIndex()]:
                rightCount += 1
        performance = Performance()
        performance.setPerf(rightCount, len(inData.getExamples().getExamplesList()))
        return performance

    def __str__(self):
        return str(self.root)

class Node(object):

    def __init__(self):
        self.children = []
        self.label = -1.0
        self.attribute = -1.0

    def __str__(self):
        return "LABEL: " + str(self.label) + " ATTRIB: " + str(self.attribute) +  str(self.children)

class backprop(Classifier):

    def __init__(self, *args):
        super(backprop, self).__init__(*args)

    def train(self, inDataSet):
        pass

    def classify(self, input):
        pass

    def __str__(self):
        pass

