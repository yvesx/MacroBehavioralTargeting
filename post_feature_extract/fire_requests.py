#!/usr/bin/python
# python ./fire_requests.py 309506851302 > bmw.json# bmw
# python ./fire_requests.py 134615383218473 > bk.json# BK
# python ./fire_requests.py 7224956785 > samsung.json # samsung mobile
# python ./fire_requests.py 211718455520845 > visa.json # visa

import sys
import os
import MySQLdb
import string
import time
import config
import random
import pymongo
#from pymongo import MongoClient
import json
import urllib2
import urllib

config = config.config()
cursor_s = config.cursor_s

fb_id = str(sys.argv[1])

def returnListOfFBIDs():
  listOfID = {}
  query = "SELECT fb_id, fb_name , category FROM %s.priority WHERE priority > 0" % (config.db)
  try:
    cursor_s.execute(query)
  except:
    print "error reading fb_id from table" 

  for i in xrange(cursor_s.rowcount):
    row = cursor_s.fetchone()
    try:
      fb_name = unicode(row[1], errors='ignore')
    except:
      fb_name = u""
    try:
      category = unicode(row[2], errors='ignore')
    except:
      category = u""
    listOfID[str(row[0])] =  {"fb_name":fb_name , "category":category}

  query = "SELECT fb_id, fb_name , category FROM %s.priority WHERE category LIKE 'tv%'" % (config.db)
  try:
    cursor_s.execute(query)
  except:
    print "error reading fb_id from table" 

  for i in xrange(cursor_s.rowcount):
    row = cursor_s.fetchone()
    try:
      fb_name = unicode(row[1], errors='ignore')
    except:
      fb_name = u""
    try:
      category = unicode(row[2], errors='ignore')
    except:
      category = u""
    listOfID[str(row[0])] =  {"fb_name":fb_name , "category":category}
  return listOfID

#assume sorted list
def findLargestNegative(lst, num):
  lst = [x - num for x in lst]
  lst = [x for x in lst if x < 0]
  #lst.sort()
  if len(lst) > 0:
    return -lst[-1]
  else:
    return 0
def getPosts(fbid):
  listOfPosts = []
  unix_stamps = []

  # careful. post_date and everyone not indexed.
  query = "SELECT post_id, post_message , UNIX_TIMESTAMP(post_date), num_of_post_likes , num_of_comments , num_of_shares ,\
                  post_type FROM %s.%s%s WHERE everyone =0 ORDER BY post_date DESC LIMIT 100" % (config.db , fbid , config.suffix)
  try:
    cursor_s.execute(query)
  except:
    print "error reading fb_id from table" 

  for i in xrange(cursor_s.rowcount):
    row = cursor_s.fetchone()
    try:
      post_message = row[1].encode('utf-8')
    except:
      post_message = u"unicode error"
    if row[6] == "NA":
      post_type = "status"
    else:
      post_type = row[6]
    post = { "fb_id": fbid,
             "post_id": row[0],
             "text": post_message,
             "unix_stamp": int(row[2]),
             "num_of_post_likes": int(row[3]),
             "num_of_comments": int(row[4]),
             "num_of_shares": int(row[5]),
             "post_type": post_type
            }
    unix_stamps.append(int(row[2]))
    listOfPosts.append(post)

  # need to get the time_since_last_post variable.
  unix_stamps.sort()
  for post in listOfPosts:
    post["time_since_last_post"] = findLargestNegative(unix_stamps,post["unix_stamp"])
  return listOfPosts


posts = getPosts(fb_id)
print json.dumps(posts)
cursor_s.close()
req=urllib2.Request(config.endpoint, 
                    json.dumps(posts), 
                    {'Content-Type': 'application/json'} )
#f = urllib2.urlopen(req)
#print f.read()
