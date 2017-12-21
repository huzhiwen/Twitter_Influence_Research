import tweepy
import csv
import random
import sys
import ssl

import time
import schedule



	# i = 0
	# schedule.every(10).seconds.do(job,lst = data_list, num = i)

	# while 1:
	#     schedule.run_pending()
	#     time.sleep(1)
consumer_key = "QWtO03bh0LPXJU9EEqRLRxNDf"
consumer_secret = "1bcjZa0mzulIzglSaraVUqnA4rg7uLjIJYdIwEPfQsFHJmlrr6"
access_key = "1887912716-vvcnGzz3cnM36F3qmkAlZWeGjTuce6fTNiz4WSi"
access_secret = "z0UtoLnuu8QslsSlmTkykX0KDnCk6iDmMXuh7SF4fGcNe"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':

	
	path = open('./../data/100/user_nodes.csv', 'r')
	data = csv.reader(path)
	headers = data.next()
	data_list = list(data)

	arg2 = int(sys.argv[1])
	arg3 = int(sys.argv[2])
	f= open('twitter_followers3.txt','w')

	for i in range(arg2,arg3):
		try:
			print "users is :"
			print data_list[i][1]
			print "Number of followers are:."
			followers = api.friends_ids(data_list[i][0])
			print len(followers)
			f.write(str(data_list[i][1]) + "	" + str(len(followers)) +"\n")



		except tweepy.error.RateLimitError:
			print 'Rate Limit Sleep.....'
			time.sleep(60*15+2)
		except tweepy.TweepError:
			print "Failed to run the command on that user, Skipping..."
	f.close()