#!/usr/bin/python
# get post activities vs post frequency.
# ./getActivities.py /tmp/file.csv
import sys
import os
import MySQLdb
import string
import time
import random
import json
import urllib2
import urllib
import numpy

import config


conf = config.config()
cursor_s = conf.cursor_s

def getBigWalls():
  listOfID = {}
  query = "SELECT fb_id,fb_name,fid FROM fb_fe.category WHERE fid> 0 ORDER BY fid ASC LIMIT 20"
  try:
    cursor_s.execute(query)
  except:
    print "error reading fb_id from table" 

  for i in xrange(cursor_s.rowcount):
    row = cursor_s.fetchone()
    listOfID[str(row[0])] = { "fb_name":row[1], "fid":row[2]}
  return listOfID

def getActivities(listOfID,filename="/tmp/foo.csv"):
  retval = []
  for fbid in listOfID.keys():
    # filter out reply posts
    retval.append([ 'Brand' , 'posts', 'likes','comments', 'shares' , 'date' ])
    query = "SELECT COUNT(post_id),SUM(num_of_post_likes),SUM(num_of_comments),SUM(num_of_shares), \
             YEAR(post_date), MONTH(post_date) FROM voxsup_facebook_frontend.%s_post_id_dim \
             WHERE num_of_post_likes > 10 AND num_of_comments > 10\
             GROUP BY YEAR(post_date), MONTH(post_date)" % (fbid)
    try:
      cursor_s.execute(query)
    except:
      print "error reading fb_id from table" 

    for i in xrange(cursor_s.rowcount):
      row = cursor_s.fetchone()
      retval.append([ filter(str.isalnum, listOfID[fbid]['fb_name']) , str(row[0]) , str(row[1]) , str(row[2]) , str(row[3]) , "%s/%s" %(row[4],row[5])  ])
    
    numpy.savetxt(filename, numpy.array(retval), delimiter=",",fmt="%s")

def getLikes(listOfID,filename="/tmp/foo.csv"):
  retval = []
  for fbid in listOfID.keys():
    seen_date = set()
    # filter out reply posts
    retval.append([ 'Brand' , 'wall_likes' , 'date' ])
    query = "SELECT likes, YEAR(date), MONTH(date) FROM fb_fe.fans WHERE fid=%s \
             GROUP BY YEAR(date), MONTH(date)" % (listOfID[fbid]['fid'])
    try:
      cursor_s.execute(query)
    except:
      print "error reading fid from table" 

    for i in xrange(cursor_s.rowcount):
      row = cursor_s.fetchone()
      if ("%s/%s" %(row[1],row[2]) not in seen_date):
        retval.append([ filter(str.isalnum, listOfID[fbid]['fb_name']) , str(row[0]) , "%s/%s" %(row[1],row[2]) ])
        seen_date.add("%s/%s" %(row[1],row[2]))
    query = "SELECT likes, YEAR(date), MONTH(date) FROM voxsup_facebook_frontend.fans WHERE fb_id=%s \
             GROUP BY YEAR(date), MONTH(date)" % (fbid)
    try:
      cursor_s.execute(query)
    except:
      print "error reading fb_id from table" 

    for i in xrange(cursor_s.rowcount):
      row = cursor_s.fetchone()
      if ("%s/%s" %(row[1],row[2]) not in seen_date):
        retval.append([ filter(str.isalnum, listOfID[fbid]['fb_name']) , str(row[0]) , "%s/%s" %(row[1],row[2]) ])
        seen_date.add("%s/%s" %(row[1],row[2]))
    numpy.savetxt(filename, numpy.array(retval), delimiter=",",fmt="%s")


#getActivities(getBigWalls(), sys.argv[1])
getLikes(getBigWalls(), sys.argv[1])