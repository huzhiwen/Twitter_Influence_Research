import json
import argparse
import csv
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
        help = 'path to json data file')

    return parser.parse_args()


def main():
	args = parse_args()
	tweets = []
	for line in open(args.file, 'r'):
		tweets.append(json.loads(line))

	tweets_json = json.dumps(tweets, indent = 4, separators = (',',':'))
	f1 = open('./data/pretty_tweets.json', 'w')
	f1.write(tweets_json)
	f1.close()


if __name__ == '__main__':
    main()