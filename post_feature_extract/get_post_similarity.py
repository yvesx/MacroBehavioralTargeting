#!/usr/bin/python
# python get_post_similarity.py 309506851302 bmw_post_sim.json # find similarity matrix & store it in file
# python get_post_similarity.py put bmw_post_sim.json # put file to mongo
# python get_post_similarity.py scipy bmw_post_sim.json bmw.json matlab_matrix.mat

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

# MATLAB-ready feaure encoding from post features
def getPostFeature(PU_keys,json):
  encodedPostFeature = {}
  encodedPostFeatureList = []
  for post in json:
    if post['post_id'] in PU_keys:
      try:
        num_of_shares = post['num_of_shares']
      except:
        num_of_shares = 0
      try:
        name_entities = len(post['name_entities'])
      except:
        name_entities = 0
      try:
        ask_share = post['ask_share']
      except:
        ask_share = 0      
      try:
        if post['post_type'] == "photo":
          post_type = 1
        else:
          post_type = 0
      except:
        post_type = 0  
      try:
        num_of_comments = post['num_of_comments']
      except:
        num_of_comments = 0    
      try:
        DOW = post['DOW']
      except:
        DOW = -1   
      try:
        exclamation = post['exclamation']
      except:
        exclamation = 0
      try:
        hash_tag = post['hash_tag']
      except:
        hash_tag = 0
      try:
        ask_like = post['ask_like']
      except:
        ask_like = 0
      try:
        time_since_last_post = post['time_since_last_post']
      except:
        time_since_last_post = -1     
      try:
        question = post['question']
      except:
        question = 0  
      
      POS_V = 0
      POS_N = 0
      POS_A = 0
      try:
        POS = len(post['POS'])
        for part in post['POS']:
          if part["pos"] == "V":
            POS_V += 1
          elif part["pos"] == "N":
            POS_N += 1
          elif part["pos"] == "A":
            POS_A += 1            
      except:
        POS = 0 
      try:
        long_text = post['long_text']
      except:
        long_text = 0
      try:
        HOD = post['HOD']
      except:
        HOD = -1  
      try:
        hyper_link = post['hyper_link']
      except:
        hyper_link = -1  
      try:
        negatives = len(post['negatives'])
      except:
        negatives = 0      
      try:
        positives = len(post['positives'])
      except:
        positives = 0        
      try:
        num_of_post_likes = post['num_of_post_likes']
      except:
        num_of_post_likes = 0 
      try:
        MOY = post['MOY']
      except:
        MOY = -1 
      try:
        contains_upper_case = post['contains_upper_case']
      except:
        contains_upper_case = 0 
      encodedPostFeature[post['post_id']] = [num_of_shares,name_entities,ask_share,
                      post_type,num_of_comments,DOW,exclamation,hash_tag,ask_like,time_since_last_post,
                      question,POS,POS_V,POS_N,POS_A,long_text,HOD,hyper_link,negatives,positives,num_of_post_likes,
                      MOY,contains_upper_case]

  for key in PU_keys:
    try:
      encodedPostFeatureList.append(encodedPostFeature[key])
    except:
      encodedPostFeatureList.append([0,0,0,0,0,
                                     0,0,0,0,0,
                                     0,0,0,0,0,
                                     0,0,0,0,0,
                                     0,0,0]) # 23-d vector
  return encodedPostFeatureList
                      
def PutMongo(array):
  mongo_collection = config.mongo_matrix_collection
  mongo_collection.insert(array,continue_on_error=True)
  

if (str(sys.argv[1]) == 'put'):
  import config
  config = config.config()
  m = buildSimMatrix(pickle.load(open(sys.argv[2],"rb")))
  PutMongo(m)
elif (str(sys.argv[1]) == 'scipy'):
  #from sklearn.cluster import KMeans, MiniBatchKMeans
  import numpy, scipy.io
  PU = pickle.load(open(sys.argv[2],"rb"))
  json = json.load(open(sys.argv[3]))
  ftr_lst = getPostFeature(PU.keys(),json)

  dense = buildNonSparseFeature(PU)
  scipy.io.savemat(sys.argv[4], mdict={'dense': dense,'ftr_lst': ftr_lst})
  #km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1)
  #km.fit(dense)
  #pickle.dump( dense, open( sys.argv[3], "wb" ) )
  # bla
else:
  import config
  config = config.config()
  cursor_s = config.cursor_s
  fb_id = str(sys.argv[1])
  PU = getPostsResponse(fb_id)
  pickle.dump( PU, open( sys.argv[2], "wb" ) )

