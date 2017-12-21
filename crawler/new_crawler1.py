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
consumer_key = "IchHORDXNmLWOJxVi6yByVChM"
consumer_secret = "394XbmdArsikKSYJOACvuTn1Yp1z2lMyjweUbSugcvK4X8Umdb"
access_key = "505945289-jjMOfE8xrEVVfxfiy4I79b0OKRvfARgjTtsCIz0Y"
access_secret = "2ifFifM4o0bAJAzF69E6g5MQVN2Z9rIkHDuq1OkRiA8tq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':

	
	path = open('./../data/100/user_nodes.csv', 'r')
	data = csv.reader(path)
	headers = data.next()
	data_list = list(data)

	arg1 = int(sys.argv[1])
	# arg2 = int(sys.argv[2])
	f= open('twitter_followers1.txt','w')

	for i in range(0,arg1):
		try:
			print "users is :"
			print data_list[i][1]
			print "Number of followings are:."
			followers = api.friends_ids(data_list[i][0])
			print len(followers)
			f.write(str(data_list[i][1]) + "	"  +  str(len(followers)) +"\n")



		except tweepy.error.RateLimitError:
			print 'Rate Limit Sleep.....'
			time.sleep(60*15+2)
		except tweepy.TweepError:
			print "Failed to run the command on that user, Skipping..."
	f.close()

