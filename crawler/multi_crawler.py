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



tokens = []
with open("access_token.txt") as file:
    for line in file: 
        line = line.strip()
        line = line.split(",")
        tokens.append(line) 
file.close()
no_token = len(tokens)


def print_user(token_n, query_user_id):

    #setting up Twitter API
    consumer_key = tokens[token_n][0]
    consumer_secret = tokens[token_n][1]
    access_key = tokens[token_n][2]
    access_secret = tokens[token_n][3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    user_b_followers = api.friends_ids(query_user_id)
    print len(user_b_followers)
    print 'Token No.', token_n, '\n'


    

if __name__ == '__main__':
	path = open('./../data/100/user_nodes.csv', 'r')
	r = int(sys.argv[1])
	data = csv.reader(path)
	headers = data.next()
	data_list = list(data)

	i = 0  # which token
	count = 1

	for k in range(r, min(len(data_list),r+15)):
		try:
			print data_list[k][1],i,count
			print_user(9, data_list[k][0])
		except tweepy.error.RateLimitError:
			print 'rate limit'
		if i == 9:  # all tokens have benn run 1 time.
		    count = count + 1
		if count % 15 == 0:  # all tokens run for 15 times
		    time.sleep(60*15)
		i = (i + 1) % 10