#!/usr/bin/python
# tweets promotion baseline algorithm
# let us assume each user's retweet action is modeled by Gamma
# and in the situation of lacking data, we for now assume users and homogeneous.
# A simplified verions of patented MBT algorithm
import sys
import os
import string
import json
import numpy as np
import math
import random
# 1: promote, -1: not to promote, 0: it doesn't know what to do.

#@@@@@@ TO USERS@@@@@@@@
#
#
# only need to modify SAMPLE, DATA,MCMCsteps,RESULTS
#
#
# assume all tweets from the same account and therefore their reach is assumeds to be equal.
# sample data contains multiple tweets. each tweet can have different number of datapoints.
SAMPLE= 1000 # REACH should be larger and any value_dimension values.
MCMCsteps = 500
DATA={ # cd1: cost_dimension_1, vd1: value_dimension_1
        "tweet1":[{'cd1':10,'vd1':12},
                  {'cd1':20,'vd1':42},
                  {'cd1':60,'vd1':72}],
        "tweet2":[{'cd1':12,'vd1':15}],
        "tweet3":[{'cd1':102,'vd1':105}],
        "tweet4":[{'cd1':322,'vd1':150}] }
METRIC = {"cost_dimension_1":"time_elapsed_since_creation","value_dimension_1":"num_of_retweets"} # FYI
INIT_GAMMA={"shape":2.,"scale":2.} # initial Gamma distribution
RESULTS = {"tweet1":0,
           "tweet2":0,
           "tweet3":0,
           "tweet4":0}
# for tweet1: x1,...,x12 <= 10, 10< x13,...,x42<=20,
#             20 < x43,....x10000 < 200000
# all xi's are iid Gamma. The goal is to estimate Gamma's parameters
def drawGammaTest( shape, scale ):
    s = np.random.gamma(shape, scale, SAMPLE)
    for t in DATA.keys():
        for row in DATA[t]:
            cut_off = row['cd1']
            # count the samples, whose response time is below cut off
            res = sum([1 if val < cut_off else 0 for val in s ])
            if res >= row['vd1']:
                RESULTS[t] += 1 # being greater than means meets or exceeds expectation
            else:
                RESULTS[t] -= 1

    ### RESULTS = {"tweet1":1,"tweet2":1,.....}
    #return sum(RESULTS) # 
def MCMCitr( steps ):
    for i in xrange(steps):
        if (INIT_GAMMA['shape'] > 0 and INIT_GAMMA['scale'] > 0 ):
            drawGammaTest(INIT_GAMMA['shape'],INIT_GAMMA['scale'])
        INIT_GAMMA['shape'] += random.random() - 0.44
        INIT_GAMMA['scale'] += random.random() - 0.44
        if i%10 == 0:
            print RESULTS

MCMCitr(MCMCsteps)