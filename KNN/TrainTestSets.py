from DataSet import DataSet


class TrainTestSets(object):

    def __init__(self, *args):
        self.train = DataSet()
        self.test = DataSet()
        self.setOptions(args)

    def getTrainingSet(self):
        return self.train

    def getTestingSet(self):
        return self.test

    def setTrainingSet(self, inTrain):
        self.train = inTrain

    def setTestingSet(self, inTest):
        self.test = inTest

    def setOptions(self, arguments):
        newDataSet = DataSet()
        for num in range(0, len(arguments)):
            if arguments[num] == "-t":
                newDataSet.load(arguments[num+1])
                self.setTestingSet(newDataSet)
                break
            elif arguments[num] == "-T":
                newDataSet.load(arguments[num+1])
                self.setTrainingSet(newDataSet)
                break

    def __print__(self):
        self.train.__print__()
        self.test.__print__()