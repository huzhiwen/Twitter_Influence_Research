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




consumer_key = "R6JmulCfPV8lrGoyqsChf8htt"
consumer_secret = "cV1cyPmLTRm0DKlOlLHKAToSPXUrJP2EDQRCYq2zJUm3ummRG2"
access_key = "940107923627241472-yyn0ZqprmXZ9ml8Yg6pvjqVloKWX0qg"
access_secret = "RN3ZYlo6dHzFk1NpE1Ztxo8pagjgHNySkiR9zUdqpJ5sI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':

	
	path = open('./../data/100/user_nodes.csv', 'r')
	data = csv.reader(path)
	headers = data.next()
	data_list = list(data)

	arg1 = int(sys.argv[1])
	arg2 = int(sys.argv[2])
	f= open('twitter_followers2.txt','w')

	for i in range(arg1,arg2):
		try:
			print "users is :"
			print data_list[i][1]
			print "Number of followings are:."
			followers = api.friends_ids(data_list[i][0])
			print len(followers)
			f.write(str(data_list[i][1]) + "	"  + str(len(followers)) +"\n")



		except tweepy.error.RateLimitError:
			print 'Rate Limit Sleep.....'
			time.sleep(60*15+2)
		except tweepy.TweepError:
			print "Failed to run the command on that user, Skipping..."
	f.close()