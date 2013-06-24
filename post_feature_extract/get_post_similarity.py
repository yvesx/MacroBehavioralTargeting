#!/usr/bin/python
# python get_post_similarity.py 309506851302 bmw_post_sim.json
# python get_post_similarity.py put bmw_post_sim.json
# python get_post_similarity.py scipy bmw_post_sim.json bmw_dense_feature.json

import sys
import os
import string
import time
import random
#import pymongo
#from pymongo import MongoClient
import json
import urllib2
import urllib
import itertools
import cPickle as pickle


def getPostsResponse(fbid):
  listOfPosts = []
  PostsUsers = {}

  # many page posts are just replies to user comments due to the crippled conversation structure at FB
  query = "SELECT post_id FROM %s.%s%s WHERE \
  everyone =0 AND num_of_comments > 0 AND num_of_post_likes > 0 AND num_of_shares > 0 \
  ORDER BY post_date DESC LIMIT 130" % (config.db , fbid , config.suffix)
  try:
    cursor_s.execute(query)
  except:
    print "error reading fb_id from table" 

  for i in xrange(cursor_s.rowcount):
    row = cursor_s.fetchone()
    listOfPosts.append(str(row[0]))

  for pid in listOfPosts:
    userIDs = set()
    query = "SELECT user_id FROM %s.%s%s WHERE post_id='%s'\
             LIMIT 10000" % (config.db , fbid , config.comment_suffix,pid)
    try:
      cursor_s.execute(query)
    except:
      print "error reading comment table" 
    for i in xrange(cursor_s.rowcount):
      row = cursor_s.fetchone()
      userIDs.add(row[0])
    # post_id is not in general index.
    query = "SELECT user_id FROM %s.%s%s WHERE post_id='%s'\
             LIMIT 10000" % (config.db , fbid , config.pl_suffix,pid)
    try:
      cursor_s.execute(query)
    except:
      print "error reading comment table" 
    for i in xrange(cursor_s.rowcount):
      row = cursor_s.fetchone()
      userIDs.add(row[0])

    PostsUsers[pid] = userIDs
  return PostsUsers

def buildSimMatrix(PostsUsers):
  matrix = []
  pids = PostsUsers.keys()
  for pair in itertools.combinations(pids,2):
    comm = len(PostsUsers[pair[0]] & PostsUsers[pair[1]])
    matrix.append({"post1":pair[0],
                   "post2":pair[1],
                   "common":comm,
                   "post1_size":len(PostsUsers[pair[0]]),
                   "post2_size":len(PostsUsers[pair[1]])})
  return matrix

def buildNonSparseFeature(PostsUsers):
    unique_user_ids = set()
    array_to_scipy = []
    for key in PostsUsers.keys():
      unique_user_ids = unique_user_ids.union(PostsUsers[key])
    for key in PostsUsers.keys():
        access_set = PostsUsers[key]
        mask = [ 1 if uid in access_set else 0 for uid in unique_user_ids ]
        # only keeyp nonsparse ones.
        array_to_scipy.append(mask)
    return array_to_scipy

def PutMongo(array):
  mongo_collection = config.mongo_matrix_collection
  mongo_collection.insert(array,continue_on_error=True)
  

if (str(sys.argv[1]) == 'put'):
  import config
  config = config.config()
  m = buildSimMatrix(pickle.load(open(sys.argv[2],"rb")))
  PutMongo(m)
elif (str(sys.argv[1]) == 'scipy'):
  PU = buildNonSparseFeature(pickle.load(open(sys.argv[2],"rb")))
  pickle.dump( PU, open( sys.argv[3], "wb" ) )
  # bla
else:
  import config
  config = config.config()
  cursor_s = config.cursor_s
  fb_id = str(sys.argv[1])
  PU = getPostsResponse(fb_id)
  pickle.dump( PU, open( sys.argv[2], "wb" ) )

