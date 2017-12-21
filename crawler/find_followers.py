#!/bin/sh

#  streaming.py

#
#  
#
import tweepy
import csv
import random
import sys
import ssl
import time


#setting up Twitter API
consumer_key = "UsaGEi6qecUrNeJ5bvdRO1yQD"
consumer_secret = "dbO5QKRneNApN6Q2ynp4Eyjz3GR0deP2NVwSfZGoRQET1fDsQn"
access_key = "1887912716-8Fk42S8KXgcOSxJFCq1sMIr90XWV7flvNHAEgDL"
access_secret = "o7nK67jE1czHKHAa32LRoKShWvLxBaBFekFGLXhx8YPMx"

#method to get a user's tweets
#def get_tweets(id_str):
   
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':  
    #get tweets for username passed at command line
	sleeptime = 4
	pages = tweepy.Cursor(api.followers, screen_name="TurkeyHu").pages()


	while True:
	    try:
	        page = next(pages)
	        time.sleep(sleeptime)
	    except tweepy.TweepError: #taking extra care of the "rate limit exceeded"
	        time.sleep(60*15) 
	        page = next(pages)
	    except StopIteration:
	        break
	    for user in page:
	       print(user.id_str)
	       print(user.screen_name)
	       print(user.followers_count)
