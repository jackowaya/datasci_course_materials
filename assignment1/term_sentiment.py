import sys
import json
from collections import defaultdict

# We define sentiment score for a word as avg(sentiment score of all tweets in which this word occurs where tweet sentiment != 0)

# Kind of a stupid way to do this, but matches
PUNCTUATION_TO_TRIM = ".,?!\"'[]_+-=\()$%^&*;:"

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def build_sentiment(sent_fp):
    result = defaultdict(float)
    for line in sent_fp:
        parts = line.decode("utf-8").split("\t")
        result[parts[0]] = float(parts[1])
    return result

def handle_tweets(tweet_fp, sentiment):
    word_sentiment_observations = defaultdict(list)
    for line in tweet_fp:
        tweet_json = json.loads(line)
        if "text" not in tweet_json:
            # Could be a delete.
            continue
        tweet_text = tweet_json["text"]
        tweet_text.lower()
        total = 0.0
        tweet_words = tweet_text.split()
        all_words = set()
        # Figure out which terms are in this tweet. Multiple-word phrases from the sentiment file are not handled
        for w in tweet_words:
            # Remove trailing punctuation
            w = w.lstrip(PUNCTUATION_TO_TRIM).rstrip(PUNCTUATION_TO_TRIM)
            if w != "":
                total += sentiment[w]
                all_words.add(w)
            
        if total != 0.0:
            # We have a sentiment score for this tweet, register this as a sentiment observation for each word 
            for w in all_words:
                if w not in sentiment or sentiment[w] == 0.0:
                    word_sentiment_observations[w].append(total)

    # Ok, we've gone through all the tweets. Average each word sentiment and print it.
    for w, l in word_sentiment_observations.iteritems():
        print ("%s\t%f" % (w, sum(l) / len(l))).encode("utf-8")

def main():
    sent_file = open(sys.argv[1])
    sentiment = build_sentiment(sent_file)
    sent_file.close()
    tweet_file = open(sys.argv[2])
    handle_tweets(tweet_file, sentiment)
    tweet_file.close()

if __name__ == '__main__':
    main()
