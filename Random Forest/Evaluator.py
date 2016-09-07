from Performance import Performance
from DataSet import DataSet
from Classifier import knn
from Classifier import NaiveBayes
from Classifier import ID3
import random

class Evaluator(object):

    def __init__(self, *args):
        self.folds = 10
        self.setOptions(args)

    def evaluate(self, Classifier, *args):
        proportion = 0
        average = 0.0
        accuracies = []
        performance = Performance()
        trainingSet = DataSet()
        for num in range(0, len(args[0])):
            if args[0][num] == "-t":
                trainingSet.load(args[0][num+1])
            if args[0][num] == "-T":
                testSet = DataSet()
                testSet.load(args[0][num+1])
            if args[0][num] == "-p":
                proportion = float(args[0][num+1])
                for items in range(0, int(proportion * len(trainingSet.getExamples().getExamplesList()))):
                    trainingSet.getExamples().add(trainingSet.getExamples().getExamplesList()[items])
                trainingSet.setAttributes(trainingSet.getAttributes())
                if type(Classifier) == ID3:
                    Classifier.train(trainingSet)
                    performance = Classifier.classify(testSet)
                    return str(performance)
                else:
                    print "Error in Evaluator:evaluate"
                performance = Classifier.classify(testSet)
                return str(performance)

        for num in range(0, self.folds):
            testSet = DataSet()
            trainSet = DataSet()
            for items in trainingSet.getExamples().getExamplesList():
                randomNum = random.randint(0,self.folds-1)
                if randomNum != num:
                    testSet.getExamples().add(items)
                else:
                    trainingSet.getExamples().add(items)
            testSet.setAttributes(trainingSet.getAttributes())
            trainSet.setAttributes(trainingSet.getAttributes())
            if (len(trainingSet.attributes.attributes) > 0):
                trainSet = trainingSet
            Classifier.train(trainSet)
            tempPerformance = Classifier.classify(testSet)
            accuracies.append(tempPerformance.accuracy)
            average += tempPerformance.accuracy
            performance += tempPerformance
        return str(performance) + " +- " + str(self.stdDev(accuracies, average))

    def setOptions(self, arguments):
        for num in range(0, len(arguments[0])):
            if arguments[0][num] == "-x":
                self.folds = int(arguments[0][num+1])
            if arguments[0][num] == "-s":
                random.seed(arguments[num+1])

    def stdDev(self, accuracies, average):
        summation = 0.0
        for items in accuracies:
            summation += float((items-average/float(self.folds))**2)
        return round(float(summation**0.5)/float(self.folds),2)

