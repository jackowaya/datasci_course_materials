import sys
import json
from collections import defaultdict

# We define sentiment score for a word as avg(sentiment score of all tweets in which this word occurs where tweet sentiment != 0)

# Kind of a stupid way to do this, but matches
PUNCTUATION_TO_TRIM = ".,?!\"'[]_+-=\()$%^&*;:"

def handle_tweets(tweet_fp):
    total_words = 0
    word_count = defaultdict(int)
    for line in tweet_fp:
        tweet_json = json.loads(line)
        if "text" not in tweet_json:
            # Could be a delete.
            continue
        tweet_text = tweet_json["text"]
        tweet_text.lower()
        tweet_words = tweet_text.split()
        # Figure out which terms are in this tweet. Multiple-word phrases from the sentiment file are not handled
        for w in tweet_words:
            # Remove leading and trailing punctuation
            w = w.lstrip(PUNCTUATION_TO_TRIM).rstrip(PUNCTUATION_TO_TRIM)
            total_words += 1
            word_count[w] += 1

    # Ok, we've gone through all the tweets. Get each word frequency and print it
    for w, c in word_count.iteritems():
        print ("%s\t%f" % (w, float(c) / float(total_words))).encode("utf-8")

def main():
    tweet_file = open(sys.argv[1])
    handle_tweets(tweet_file)
    tweet_file.close()

if __name__ == '__main__':
    main()
