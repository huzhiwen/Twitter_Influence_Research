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
consumer_key = "R6OgmXfoXUPssAEA8bi02iU7I"
consumer_secret = "0GGkIGx5ncvqax4AFcW5JSYtSgx8ePYXXIDd9tkW0lblZgCyuX"
access_key = "1887912716-QNNFCAbysjEGLNZZp5PaquZ0SHivCxTCnGErx7C"
access_secret = "7Ue4yQP3rYgir1JHBDUiK3jstEjUUIaXqoED3nVre6AM4"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':

	
	path = open('./../data/100/user_nodes.csv', 'r')
	data = csv.reader(path)
	headers = data.next()
	data_list = list(data)

	arg3 = int(sys.argv[1])
	f= open('twitter_followers4.txt','w')

	for i in range(arg3,len(data_list)):
		try:
			print "users is :"
			print data_list[i][1]
			print "Number of followers are:."
			followers = api.friends_ids(data_list[i][0])
			print len(followers)
			f.write(str(data_list[i][1]) + "	"  + str(len(followers)) +"\n")


		except tweepy.error.RateLimitError:
			print 'Rate Limit Sleep.....'
			time.sleep(60*15+2)
		except tweepy.TweepError:
			print "Failed to run the command on that user, Skipping..."
	f.close()