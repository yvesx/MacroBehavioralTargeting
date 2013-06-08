#!/usr/bin/python
# python ./fire_requests.py 107939332066

import sys
import os
import MySQLdb
import string
import time
import config
import random
import pymongo
from pymongo import MongoClient
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

def getPosts():
  listOfID = {}
  query = "SELECT post_id, post_message , post_date, num_of_post_likes , num_of_comments , num_of_shares ,\
                  post_type FROM %s.%s%s LIMIT 50" % (config.db , fb_id , config.suffix)
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

listOfAllID=returnListOfFBIDs()
try:
  listOfID = {str(sys.argv[2]):listOfAllID[str(sys.argv[2])]}
except:
  listOfID=returnListOfFBIDs()
  
cursor_s.close()
for ID in listOfID.keys():
  print listOfID[ID]
  print ID
  data = {"fb_id":ID, "index":sys.argv[1]}
  req=urllib2.Request(config.endpoint, 
                      json.dumps(data), 
                      {'Content-Type': 'application/json'} )
  f = urllib2.urlopen(req)
  print f.read()
