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
    best_tag = ""
    best_score = -1
    for t, c in hashtag_counts.iteritems():
        if c > best_score:
            best_tag = t
            best_score = c
    print ("%s\t%f" % (best_tag, best_score)).encode("utf-8")

def main():
    tweet_file = open(sys.argv[1])
    handle_tweets(tweet_file)
    tweet_file.close()

if __name__ == '__main__':
    main()
