import sys
import json
from collections import defaultdict

def handle_tweets(tweet_fp):
    hashtag_counts = defaultdict(float)
    for line in tweet_fp:
        tweet_json = json.loads(line)
        if "text" not in tweet_json:
            # Could be a delete.
            continue
        tweet_tags = tweet_json["entities"]["hashtags"]
        # Figure out which terms are in this tweet. Multiple-word phrases from the sentiment file are not handled
        for t in tweet_tags:
            hashtag_counts[t["text"]] += 1
            
    # Ok, we've gone through all the tweets. Find the best hashtag
    tups = sorted(hashtag_counts.items(), key= lambda x: x[1], reverse=True)

    for i in range(10):
        if len(tups) > i:
            print ("%s\t%f" % (tups[i][0], tups[i][1])).encode("utf-8")

def main():
    tweet_file = open(sys.argv[1])
    handle_tweets(tweet_file)
    tweet_file.close()

if __name__ == '__main__':
    main()
