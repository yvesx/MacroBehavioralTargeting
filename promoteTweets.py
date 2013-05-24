#!/usr/bin/python
# tweets promotion baseline algorithm
# let us assume each user's retweet action is modeled by Gamma
# and in the situation of lacking data, we for now assume users and homogeneous.
# A simplified verions of patented MBT algorithm
import sys
import os
import MySQLdb
import string
import json
import numpy as np
import math
# 1: promote, -1: not to promote, 0: it doesn't know what to do.

# assume all tweets from the same account and therefore their reach is assumeds to be equal.
# sample data contains multiple tweets. each tweet can have different number of datapoints.
METRIC = {"cost_dimension_1":"time_elapsed_since_creation","value_dimension_1":"num_of_retweets"} # FYI
REACH = 10000 # REACH should be larger and any value_dimension values.
SAMPLE={ # cd1: cost_dimension_1, vd1: value_dimension_1
        "tweet1":[{'cd1':10,'vd1':12},
                  {'cd1':20,'vd1':42},
                  {'cd1':60,'vd1':72}],
        "tweet2":[{'cd1':12,'vd1':15}],
        "tweet3":[{'cd1':102,'vd1':105}],
        "tweet4":[{'cd1':322,'vd1':150}] }

def estimateLambda(data):



