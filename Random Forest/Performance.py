class Performance(object):


    def __init__(self):
        self.accuracy = 0.0
        self.rightCount = -1.0
        self.totalCount = -1.0

    def __iadd__(self, inPerformance):
        newPerformance = Performance()
        newRightCount = self.rightCount + inPerformance.rightCount
        newTotalCount = self.totalCount + inPerformance.totalCount
        newPerformance.setPerf(newRightCount, newTotalCount)
        return newPerformance

    def setPerf(self, rightCount, totalCount):
        self.rightCount = rightCount
        self.totalCount = totalCount
        self.accuracy = round((float(rightCount)/float(totalCount))*100,2)

    def __str__(self):
        return str(self.accuracy)