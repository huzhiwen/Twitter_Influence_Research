import tweepy
import sys
import jsonpickle
import ConfigParser
import argparse
'''
This python file use twitter search api to crawl data base on user input query. Output in json format
@output: tweets.json
'''

'''
@return: arguments that user pass in.
  flag: -w: the number of tweets that user want to crawl
        -p: tweets per query
'''

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--tweets_wanted', default=1000, type=int,
                        help='how many tweets you want to crawl')
    parser.add_argument('-p', '--tweets_per_query', default=100, type=int,
                        help='the tweets per query')
    parser.add_argument('-q', '--query', default='ucla', type=str,
                        help='the query')
    parser.add_argument('-f', '--file_path', default='tweets.json', type=str,
                        help='the file path for tweets')
    return parser.parse_args()



# Specify config file
config = ConfigParser.RawConfigParser()
config.read('crawler.cfg')

# Reading Twitter API key and secret from config file
API_KEY = config.get('twitter', 'consumer_key')
API_SECRET = config.get('twitter', 'consumer_secret')

# Reading Twitter specify language from config file
language = config.get('twitter', 'language')


# authenticate and using tweepy as a api
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

# if there is a problem with api key and api secret
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)



# ask user to input their query. And using Twitter search API
# query = raw_input('Please enter your query: ')

args = parse_args()
query = args.query

# how many tweets you want to crawl
tweets_wanted = args.tweets_wanted

#the tweets per query
tweets_per_query = args.tweets_per_query

# json file to store data
# tweets_filepath = 'tweets.json'
tweets_filepath = args.file_path



# Returns results with an ID greater than (that is, more recent than) the specified ID. There are limits to the number of Tweets which can be accessed through the API. If the limit of Tweets has occured since the since_id, the since_id will be forced to the oldest ID available.
# None stands for no lower limit, go as far back as API allows
sinceId = None

# Returns results with an ID less than (that is, older than) or equal to the specified ID.
max_id = -1L

# Note down crawling information
tweetCount = 0
print 'Searching for:'  + query
print 'Start crawling {0} tweets'.format(tweets_wanted)

with open(tweets_filepath, 'w') as f:
    while tweetCount < tweets_wanted:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    # start using twitter search api call, set q equal to the information that user just enter
                    # set count equal to number of tweets that each query need to get
                    new_tweets = api.search(q=query, count=tweets_per_query)
                else:
                    new_tweets = api.search(q=query, count=tweets_per_query, since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=query, count=tweets_per_query, max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=query, count=tweets_per_query,max_id=str(max_id - 1), since_id=sinceId)

            # if there is no tweets
            if not new_tweets:
                print("No more tweets found")
                break

            # write to json file
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Got {0} tweets".format(tweetCount))

            # set max_id to the most recent tweets
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print(str(e))
            break

print "Got {0} tweets in total".format(tweetCount)

