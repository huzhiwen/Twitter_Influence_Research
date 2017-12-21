import json
import argparse
import csv
from datetime import datetime

TWEET_NODE_TEXT_LENGTH = 200


# removing http links, letters not in ASCII
def clean_text(tweet):
    if ('urls' in tweet['entities']) or ('media' in tweet['entities']) or ('user_mentions' in tweet['entities']):
        index_to_remove = []
        if 'urls' in tweet['entities']:            
            for url in tweet['entities']['urls']:
                index_to_remove.append(url['indices'])
        if 'media' in tweet['entities']:
            for url in tweet['entities']['media']:
                index_to_remove.append(url['indices'])
        if 'user_mentions' in tweet['entities']:
            for url in tweet['entities']['user_mentions']:
                index_to_remove.append(url['indices'])
            
        index_to_remove = sorted(index_to_remove)
        print tweet['id_str']
        print index_to_remove

        text = tweet['text']
        write_text = ''

        if len(index_to_remove) == 1:
                write_text = text[0:index_to_remove[0][0]] + text[index_to_remove[0][1]:]
        else:
            for index, url_i in enumerate(index_to_remove):
                # print index
                # print url_i
                if index == 0:
                    write_text += text[0:url_i[0]]
                elif index == len(index_to_remove) - 1:
                    write_text += text[index_to_remove[index-1][1]:url_i[0]]
                    write_text += text[url_i[1]:]
                else:
                    write_text += text[index_to_remove[index-1][1]:url_i[0]]
        
    else:
        write_text = tweet['text']
    # write_text.replace('\n',' ').replace(',',' ').encode('utf8')
    # print write_text
    
    if 'retweeted_status' in tweet:
        write_text = write_text[2:]

    write_text = write_text.replace('\n',' ').replace(',',' ').replace('@',' ').replace('#',' ').replace(':','')

    write_text = ''.join([i if ord(i) < 128 else ' ' for i in write_text])
    print write_text
    return write_text.lstrip()


# if the tweet does not meet some condition, we jump over to the next tweet.
def jump_tweet(tweet):
    # some lines are not tweets, jump over them        
    if ('id' not in tweet):
        return True

    # if this tweet is not quoted by someone or does not have hashtag,
    # or does not mention user, continue the for loop
    if (('quoted_status' not in tweet) and 
        (not tweet['entities']['hashtags']) and 
        (not tweet['entities']['user_mentions']) and 
        ('retweeted_status' not in tweet)):
        return True

    if (tweet['lang'] <> "en"):
        return True

    return False

# parse each tweet
def parse_tweet(tweet, file_config, user_nodes, tweet_nodes, tweet_texts, hashtag_nodes):
    
    # write user id and tweet id to user_tweet_edge
    lw = tweet['user']['id_str'] + ',' + tweet['id_str'] \
        + ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
    file_config['file_ute'].write(lw + "\n")

    # extract fields id_str,screen_name,followers_count,lang for user_node
    user_nodes[tweet['user']['id_str']] = "{0},{1}".format(
        tweet['user']['id_str'],
        tweet['user']['screen_name'])
    # ,   tweet['user']['followers_count'],
        # tweet['user']['lang'])

    # extract fields id_str, text for original tweet to tweet_node
    tweet_nodes[tweet['id_str']] = "{0},{1}".format(
        tweet['id_str'], tweet['text'][:TWEET_NODE_TEXT_LENGTH].replace('\n',' ').replace(',',' ').encode('utf8'))

    tweet_texts[tweet['id_str']] = clean_text(tweet)
    # tweet_texts[tweet['id_str']] = tweet['text'].replace('\n',' ').replace(',',' ').encode('utf8')

    if tweet['entities']['hashtags']:

        for item in tweet['entities']['hashtags']:
            # write tweet id and hashtag to tweet_hashtag_edge for each hashtag in hashtags

            lw = tweet['id_str'] + ',' + item['text'] \
            + ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            file_config['file_the'].write(lw.encode('utf8') + "\n")

            # write user id and hashtag to user_hashtag_edge for each hashtag in hashtags
            uhe_lw = tweet['user']['id_str'] + ',' + item['text'] \
            + ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            file_config['file_uhe'].write(uhe_lw.encode('utf8') + "\n")

        
            hashtag_nodes[item['text']] = "{0}".format(item['text'].encode('utf8'))

    if tweet['entities']['user_mentions']:

        for item in tweet['entities']['user_mentions']:
            # write into user_mention_user_edge
            lw = tweet['user']['id_str'] + ',' + item['id_str'] \
            + ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            file_config['file_umue'].write(lw + "\n")

            user_nodes[item['id_str']] = "{0},{1}".format(
            item['id_str'], item['screen_name'])



# parameters in config
# ,tweet_file, tweet_quote_edge, user_tweet_edge, tweet_hashtag_edge, user_hashtag_edge, 
# user_mention_user_edge, user_node, tweet_node, tweet_text, hashtag_node

def network_extract(config):


    user_nodes = {}
    tweet_nodes = {}
    tweet_texts = {}
    hashtag_nodes = {}

    file_config = {}

    # edge files
    file_config['file_uqe'] = open(config['user_quote_edge'], 'w')
    # file_uqe.write('Source,Target\n')
    file_config['file_ute'] = open(config['user_tweet_edge'], 'w')
    # file_ute.write('Source,Target\n')
    file_config['file_the'] = open(config['tweet_hashtag_edge'], 'w')
    # file_the.write('Source,Target\n')
    file_config['file_uhe'] = open(config['user_hashtag_edge'], 'w')
    # file_uhe.write('Source,Target\n')
    file_config['file_umue'] = open(config['user_mention_user_edge'], 'w')
    # file_umue.write('Source,Target\n')
    file_config['file_ure'] = open(config['user_retweet_edge'], 'w')


    #node files
    file_config['file_un'] = open(config['user_node'], 'w')
    file_config['file_un'].write('Id,Label\n')
    file_config['file_tn'] = open(config['tweet_node'], 'w')
    file_config['file_tn'].write('Id,Text\n')

    file_config['file_tt'] = open(config['tweet_text'], 'w')
    # file_tt.write('Id,Text\n')

    file_config['file_hn'] = open(config['hashtag_node'], 'w')
    file_config['file_hn'].write('Hashtag\n')


    fh = open(config['tweet_file'], 'r')
    #read each line in json file
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        
        if jump_tweet(tweet):
            continue

        parse_tweet(tweet, file_config, user_nodes, tweet_nodes, tweet_texts, hashtag_nodes)

        if 'quoted_status' in tweet:

            # write to edge file/ base on quoted_status
            lw = tweet['user']['id_str'] + ',' + tweet['quoted_status']['user']['id_str']+ \
                ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            file_config['file_uqe'].write(lw + "\n")

            parse_tweet(tweet['quoted_status'], file_config, user_nodes, tweet_nodes, tweet_texts, hashtag_nodes)

        if 'retweeted_status' in tweet:

            # write to edge file/ base on quoted_status
            lw = tweet['user']['id_str'] + ',' + tweet['retweeted_status']['user']['id_str']+ \
                ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            file_config['file_ure'].write(lw + "\n")

            parse_tweet(tweet['retweeted_status'], file_config, user_nodes, tweet_nodes, tweet_texts, hashtag_nodes)
   

    # write to node file
    for user, user_string in user_nodes.items():
        file_config['file_un'].write('{0}\n'.format(user_string))
    for tweet, tweet_string in tweet_nodes.items():
        file_config['file_tn'].write('{0}\n'.format(tweet_string))
    for tweet, tweet_text_string in tweet_texts.items():
        file_config['file_tt'].write('{0}\n'.format(tweet_text_string))
    for hashtag, hashtag_string in hashtag_nodes.items():
        file_config['file_hn'].write('{0}\n'.format(hashtag_string))
    
    file_config['file_uqe'].close()
    file_config['file_un'].close()
    file_config['file_tn'].close()
    file_config['file_tt'].close()
    file_config['file_hn'].close()
    file_config['file_ure'].close()
    file_config['file_ute'].close()
    file_config['file_the'].close()
    file_config['file_uhe'].close()
    file_config['file_umue'].close()
    fh.close()


def user_hashtag_links(config):
    
    user_hashtag = []
    with open(config['user_hashtag_edge']) as file:
        for line in file:
    #         line = line.replace('#','').replace('\n','')
            line = line.strip()
            line = line.split(",")
            user_hashtag.append(line)
    file.close()
    no_lines = len(user_hashtag)

    user_hashtag.sort(key=lambda x: x[2])
    
    all_hashtags = [row[1] for row in user_hashtag]
    hash_user_link = {}
    file_w = open(config['user_user_hashtag_edge'], 'w')

    for i, item in enumerate(user_hashtag):
        if not hash_user_link.has_key(user_hashtag[i][1]):
            hash_user_link[user_hashtag[i][1]] = []
        if user_hashtag[i][0] not in hash_user_link[user_hashtag[i][1]]:
            hash_user_link[user_hashtag[i][1]].append(user_hashtag[i][0])
        
        for user in hash_user_link[item[1]]:         
            if user <> item[0]:
                lw = user + ',' + item[0] + ',' + str(item[2])
                file_w.write(lw + "\n")
                
    file_w.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
        help = 'path to json data file')
    parser.add_argument('-o', '--output', default='./',
        help = 'path to the output files')

    return parser.parse_args()


# parameters in config
# ,tweet_file, tweet_quote_edge, user_tweet_edge, tweet_hashtag_edge, user_hashtag_edge, 
# user_mention_user_edge, user_node, tweet_node, tweet_text, hashtag_node

def main():
    config = {}
    args = parse_args()
    config['tweet_file'] = args.file

    # edge files
    config['user_quote_edge'] = args.output + 'edge_user_quote.csv'
    config['user_tweet_edge'] = args.output + 'edge_user_tweet.csv'
    config['tweet_hashtag_edge'] = args.output + 'edge_tweet_hashtag.csv'
    config['user_hashtag_edge'] = args.output + 'edge_user_hashtag.csv'
    config['user_mention_user_edge'] = args.output + 'edge_user_mention_user.csv'
    config['user_retweet_edge'] = args.output + 'edge_user_retweet.csv'
    config['user_user_hashtag_edge'] = args.output + 'edge_user_user_hashtag.csv'

    # node files
    config['user_node'] = args.output + 'node_user.csv'
    config['tweet_node'] = args.output + 'node_tweet.csv'
    config['tweet_text'] = args.output + 'text_tweet.csv'
    config['hashtag_node'] = args.output + 'node_hashtag.csv'

    network_extract(config)

    user_hashtag_links(config)




if __name__ == '__main__':
    main()