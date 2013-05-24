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

"""
    @@@@@@ sample output. the tweet with highest score is the best to promote. so sort the tweets in descending order
    {'tweet3': 1, 'tweet2': 1, 'tweet1': 3, 'tweet4': 1}
    {'tweet3': 11, 'tweet2': 11, 'tweet1': 33, 'tweet4': 11}
    {'tweet3': 21, 'tweet2': 21, 'tweet1': 63, 'tweet4': 21}
    {'tweet3': 31, 'tweet2': 23, 'tweet1': 81, 'tweet4': 31}
    {'tweet3': 41, 'tweet2': 13, 'tweet1': 73, 'tweet4': 41}
    {'tweet3': 51, 'tweet2': 3, 'tweet1': 63, 'tweet4': 51}
    {'tweet3': 61, 'tweet2': -7, 'tweet1': 53, 'tweet4': 61}
    {'tweet3': 71, 'tweet2': -17, 'tweet1': 43, 'tweet4': 71}
    {'tweet3': 81, 'tweet2': -27, 'tweet1': 33, 'tweet4': 81}
    {'tweet3': 91, 'tweet2': -37, 'tweet1': 23, 'tweet4': 91}
    {'tweet3': 101, 'tweet2': -47, 'tweet1': -1, 'tweet4': 101}
    {'tweet3': 111, 'tweet2': -57, 'tweet1': -31, 'tweet4': 111}
    {'tweet3': 107, 'tweet2': -67, 'tweet1': -61, 'tweet4': 121}
    {'tweet3': 97, 'tweet2': -77, 'tweet1': -91, 'tweet4': 131}
    {'tweet3': 87, 'tweet2': -87, 'tweet1': -121, 'tweet4': 141}
    {'tweet3': 77, 'tweet2': -97, 'tweet1': -151, 'tweet4': 151}
    {'tweet3': 67, 'tweet2': -107, 'tweet1': -181, 'tweet4': 161}
    {'tweet3': 57, 'tweet2': -117, 'tweet1': -211, 'tweet4': 171}
    {'tweet3': 47, 'tweet2': -127, 'tweet1': -241, 'tweet4': 181}
    {'tweet3': 37, 'tweet2': -137, 'tweet1': -271, 'tweet4': 191}
    {'tweet3': 27, 'tweet2': -147, 'tweet1': -301, 'tweet4': 201}
    {'tweet3': 17, 'tweet2': -157, 'tweet1': -331, 'tweet4': 211}
    {'tweet3': 7, 'tweet2': -167, 'tweet1': -361, 'tweet4': 221}
    {'tweet3': -3, 'tweet2': -177, 'tweet1': -391, 'tweet4': 231}
    {'tweet3': -13, 'tweet2': -187, 'tweet1': -421, 'tweet4': 241}
    {'tweet3': -23, 'tweet2': -197, 'tweet1': -451, 'tweet4': 251}
    {'tweet3': -33, 'tweet2': -207, 'tweet1': -481, 'tweet4': 261}
    {'tweet3': -43, 'tweet2': -217, 'tweet1': -511, 'tweet4': 271}
    {'tweet3': -53, 'tweet2': -227, 'tweet1': -541, 'tweet4': 281}
    {'tweet3': -63, 'tweet2': -237, 'tweet1': -571, 'tweet4': 291}
    {'tweet3': -73, 'tweet2': -247, 'tweet1': -601, 'tweet4': 301}
    {'tweet3': -83, 'tweet2': -257, 'tweet1': -631, 'tweet4': 311}
    {'tweet3': -93, 'tweet2': -267, 'tweet1': -661, 'tweet4': 321}
    {'tweet3': -103, 'tweet2': -277, 'tweet1': -691, 'tweet4': 331}
    {'tweet3': -113, 'tweet2': -287, 'tweet1': -721, 'tweet4': 341}
    {'tweet3': -123, 'tweet2': -297, 'tweet1': -751, 'tweet4': 341}
    {'tweet3': -133, 'tweet2': -307, 'tweet1': -781, 'tweet4': 331}
    {'tweet3': -143, 'tweet2': -317, 'tweet1': -811, 'tweet4': 321}
    {'tweet3': -153, 'tweet2': -327, 'tweet1': -841, 'tweet4': 311}
    {'tweet3': -163, 'tweet2': -337, 'tweet1': -871, 'tweet4': 301}
    {'tweet3': -173, 'tweet2': -347, 'tweet1': -901, 'tweet4': 291}
    {'tweet3': -183, 'tweet2': -357, 'tweet1': -931, 'tweet4': 281}
    {'tweet3': -193, 'tweet2': -367, 'tweet1': -961, 'tweet4': 271}
    {'tweet3': -203, 'tweet2': -377, 'tweet1': -991, 'tweet4': 261}
    {'tweet3': -213, 'tweet2': -387, 'tweet1': -1021, 'tweet4': 251}
    {'tweet3': -223, 'tweet2': -397, 'tweet1': -1051, 'tweet4': 241}
    {'tweet3': -233, 'tweet2': -407, 'tweet1': -1081, 'tweet4': 231}
    {'tweet3': -243, 'tweet2': -417, 'tweet1': -1111, 'tweet4': 221}
    {'tweet3': -253, 'tweet2': -427, 'tweet1': -1141, 'tweet4': 211}
    {'tweet3': -263, 'tweet2': -437, 'tweet1': -1171, 'tweet4': 201}
"""
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