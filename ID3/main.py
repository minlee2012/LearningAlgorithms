#
# Min Lee
# ml1237@georgetown.edu
# MacOS
# Python
#
# In accordance with the class policies and Georgetown's Honor Code,
# I certify that, with the exceptions of the class resources and those
# items noted below, I have neither given nor received any assistance
# on this project.
#

import sys
from Classifier import knn
from Classifier import NaiveBayes
from Classifier import ID3
from Evaluator import Evaluator
from DataSet import DataSet

from Attributes import Attributes
from Attribute import Attribute

"""
classifier = ID3(sys.argv)
evaluator = Evaluator(sys.argv)
performance = evaluator.evaluate(classifier, sys.argv)

print performance
"""

testAttributes = Attributes()
testAttribute = Attribute.factory("n")
testAttribute.setName("make")
testAttribute.addValue("cannondale")
testAttribute.addValue("nishiki")
testAttribute.addValue("trek")
testAttribute2 = Attribute.factory("n")
testAttribute2.setName("random")
testAttribute2.addValue("bc")
testAttribute2.addValue("ad")

testAttributes.add(testAttribute)
testAttributes.add(testAttribute2)
print testAttributes

newDataSet = DataSet()
newAttributes = Attributes()
for items in testAttributes.attributes:
    if len(items.domain) > 2:
        binaryDomain = bin(len(items.domain))
        print binaryDomain
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
print newAttributes
print newAttributes.classIndex
print newDataSet



classifier = ID3(sys.argv)
evaluator = Evaluator(sys.argv)
performance = evaluator.evaluate(classifier, sys.argv)

print performance

"""
testDecimal = 8
print bin(testDecimal)
for index, c in enumerate(str(bin(testDecimal))):
    if index <=1:
        pass
    else:
        print c
print "LENGTH " + str(len(str(bin(testDecimal)))-2)
"""
exit(0)