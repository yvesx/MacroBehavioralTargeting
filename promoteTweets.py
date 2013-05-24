#!/usr/bin/python
# tweets promotion baseline algorithm
# exponential parameter estimation
# using exponential cdf
import sys
import os
import MySQLdb
import string
import json
import numpy as np
import math
# 1: promote, -1: not to promote, 0: it doesn't know what to do.

# sample data contains multiple tweets. each tweet can have different number of datapoints.
METRIC = {"cost_dimension_1":"time_elapsed","value_dimension_1":"retweets"} # FYI
SAMPLE={
        "tweet1":[{'cd1':10,'vd1':12},
                  {'cd1':20,'vd1':42},
                  {'cd1':60,'vd1':72}],
        "tweet2":[{'cd1':12,'vd1':15}],
        "tweet3":[{'cd1':102,'vd1':105}],
        "tweet4":[{'cd1':322,'vd1':150}] }

def estimateLambda(data):



