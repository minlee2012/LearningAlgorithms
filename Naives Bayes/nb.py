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
from Classifier import NaiveBayes
from Evaluator import Evaluator

classifier = NaiveBayes(sys.argv)
evaluator = Evaluator(sys.argv)
performance = evaluator.evaluate(classifier, sys.argv)

print performance
