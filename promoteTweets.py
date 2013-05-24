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
# prediction until t_limit_in_sec (default 200hrs) number of seconds after post

# sample data contains multiple tweets. each tweet can have 
SAMPLE={"tweet1":[{'time_elapsed':10,'retweets':12},
                  {'time_elapsed':20,'retweets':42},
                  {'time_elapsed':60,'retweets':72}],
        "tweet2":[{'time_elapsed':12,'retweets':15}],
        "tweet3":[{'time_elapsed':102,'retweets':105}],
        "tweet4":[{'time_elapsed':322,'retweets':150}] }
REQUIRED_INSIGHT_TYPES = ['post_impressions_organic_unique', 'post_engaged_users']


def promotePost( dict_posts , t_limit_in_sec=720000 , value_dim='post_engaged_users' , cost_dim='post_impressions_organic_unique'):
    dict_result = [] # to hold final promote decision
    percentile_score =[]
    for post_id_key in dict_posts.keys():
        value_axis =[]
        cost_axis =[]
        time_axis = dict_posts[post_id_key]['insight_value_by_t'].keys()
        time_axis.sort()

        for t in time_axis:
            if t > t_limit_in_sec:
                break
            value_axis.append(dict_posts[post_id_key]['insight_value_by_t'][t][value_dim])
            cost_axis.append(dict_posts[post_id_key]['insight_value_by_t'][t][cost_dim])

        time_axis = time_axis[:len(value_axis)]
        if len(time_axis) < 3:
            # not enough data
            dict_result.append({'post_id':post_id_key ,'score':-1, 'promote':0})
            continue


        value_eval = np.trapz(value_axis, x=time_axis)
        cost_eval = np.trapz(cost_axis, x=time_axis)
        time_eval = int(time_axis[-1] - time_axis[0])
        if cost_eval > 0 and time_eval > 0:
            cur_score = float(value_eval / cost_eval) / time_eval
            percentile_score.append( cur_score ) # only put meaningful score into percentile calculation
        else:
            cur_score = -1
        dict_result.append({'post_id':post_id_key ,'score':cur_score,'promote':-1})

    if len(percentile_score) < 1:
        cut_off = sys.float_info.max
    else:
        cut_off = np.percentile(percentile_score, 90)
    return [ r if r['score']< cut_off else {'post_id':r['post_id'] ,'score':r['score'], 'promote':1} for r in dict_result ]

# take a list of tuples ( post_id , post_type , t_in_seconds , insight_dict)
def reformatPostData(list_post_stats , insight_types_chosen=REQUIRED_INSIGHT_TYPES):
    dict_posts ={}
    list_post_stats.sort(key=lambda x: x[2]) # sort by time
    for post in list_post_stats: # post = ( post_id , post_type , t_in_seconds , insight_dict)
        post_id = post[0]
        post_type = post[1]
        t_in_seconds = max(1,int(post[2]/100)*100 )# quantize
        insight_dict = post[3]
        try:
            insight_value = insight_dict['values'][0]['value']# this might be a number or dict...
            insight_type = insight_dict['name']
        except:
            insight_value = 0
            insight_type = u''
        if not isinstance( insight_value , ( int, long ) ):
            int_val = 0
            try:
                for key, value in insight_value.iteritems():
                    int_val += int(value)
            except:
                int_val = 0
            insight_value = int_val

        if not (post_id in dict_posts.keys()):
            dict_posts[post_id] = {"post_type":post_type,"insight_value_by_t":{} }

        if not (t_in_seconds in dict_posts[post_id]['insight_value_by_t'].keys()):
            dict_posts[post_id]['insight_value_by_t'][t_in_seconds] = {}

        if insight_type in insight_types_chosen:
            dict_posts[post_id]['insight_value_by_t'][t_in_seconds][insight_type] = insight_value
        # "insight_value_by_t":{ '1':{'x':1,'y':2},
        #						 '10':{'x':5,'y':9},
        #						 '20':{'x':15,'y':12}, ...
        #							}
    return dict_posts

