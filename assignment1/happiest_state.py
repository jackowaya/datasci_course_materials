import sys
import json
from collections import defaultdict

# We define sentiment score for a word as avg(sentiment score of all tweets in which this word occurs where tweet sentiment != 0)

# Kind of a stupid way to do this, but matches
PUNCTUATION_TO_TRIM = ".,?!\"'[]_+-=\()$%^&*;:"

# State name mappings via wikipedia
STATE_NAMES = {'gu': 'GU', 'n.c.': 'NC', 'tenn.': 'TN', 'del.': 'DE', 'v.i.': 'VI', 'mo.': 'MO', 'ga': 'GA', 'nevada': 'NV', 'maine': 'ME', 'kans.': 'KS', 'tx': 'TX', 'la': 'LA', 'wyoming': 'WY', 'minnesota': 'MN', 'tn': 'TN', 'maryland': 'MD', 'texas': 'TX', 'dl': 'DE', 'calif.': 'CA', 'iowa': 'IA', 'mont.': 'MT', 'michigan': 'MI', 'de': 'DE', 'utah': 'UT', 'dc': 'DC', 'georgia': 'GA', 'wash.': 'WA', 'va.': 'VA', 'rhode island': 'RI', 'n.h.': 'NH', 'hawaii': 'HI', 'vt.': 'VT', 'n. dak.': 'ND', 'district of columbia': 'DC', 'nv': 'NV', 'ohio': 'OH', 'vermont': 'VT', 'mich.': 'MI', 'us-pr': 'PR', 'wisconsin': 'WI', 'wyo.': 'WY', 'ky.': 'KY', 'oreg.': 'OR', 'oklahoma': 'OK', 'delaware': 'DE', 'n. mex.': 'NM', 'p.r.': 'PR', 'arkansas': 'AR', 'ri': 'RI', 'arizona': 'AZ', 'md.': 'MD', 'wa': 'WA', 'wn': 'WA', 'wi': 'WI', 'ill.': 'IL', 'california': 'CA', 'new mexico': 'NM', 'nebr.': 'NE', 'nev.': 'NV', 'wy': 'WY', 'ok': 'OK', 'oh': 'OH', 'florida': 'FL', 'alaska': 'AK', 'ws': 'WI', 'or': 'OR', 'co': 'CO', 'colorado': 'CO', 'cl': 'CO', 's. dak.': 'SD', 'ca': 'CA', 'us-vi': 'VI', 'washington': 'WA', 'cf': 'CA', 'ala.': 'AL', 'ga.': 'GA', 'tennessee': 'TN', 'fla.': 'FL', 'ct': 'CT', 'pr': 'PR', 'mississippi': 'MS', 'south dakota': 'SD', 'us-gu': 'GU', 'new jersey': 'NJ', 'minn.': 'MN', 'north carolina': 'NC', 'wis.': 'WI', 'new york': 'NY', 's.c.': 'SC', 'indiana': 'IN', 'louisiana': 'LA', 'us-mp': 'MP', 'west virginia': 'WV', 'ark.': 'AR', 'oregon': 'OR', 'connecticut': 'CT', 'hi': 'HI', 'colo.': 'CO', 'a.s.': 'AS', 'ha': 'HI', 'me': 'ME', 'md': 'MD', 'miss.': 'MS', 'ma': 'MA', 'conn.': 'CT', 'mc': 'MI', 'ut': 'UT', 'mo': 'MO', 'mn': 'MN', 'mi': 'MS', 'kentucky': 'KY', 'mt': 'MT', 'nebraska': 'NE', 'new hampshire': 'NH', 'mp': 'MP', 'ms': 'MS', 'south carolina': 'SC', 'n.y.': 'NY', 'va': 'VA', 'la.': 'LA', 'north dakota': 'ND', 'vi': 'VI', 'ak': 'AK', 'al': 'AL', 'ar': 'AR', 'vt': 'VT', 'il': 'IL', 'in': 'IN', 'ia': 'IA', 'okla.': 'OK', 'az': 'AZ', 'wv': 'WV', 'id': 'ID', 'nh': 'NH', 'nj': 'NJ', 'nm': 'NM', 'pa': 'PA', 'nb': 'NE', 'nc': 'NC', 'nd': 'ND', 'ne': 'NE', 'illinois': 'IL', 'ny': 'NY', 'ariz.': 'AZ', 'ind.': 'IN', 'idaho': 'ID', 'd.c.': 'DC', 'kansas': 'KS', 'virginia': 'VA', 'sc': 'SC', 'montana': 'MT', 'massachusetts': 'MA', 'fl': 'FL', 'alabama': 'AL', 'ka': 'KS', 'pennsylvania': 'PA', 'r.i.': 'RI', 'w. va.': 'WV', 'ks': 'KS', 'tex.': 'TX', 'missouri': 'MO', 'n.j.': 'NJ', 'ky': 'KY', 'mass.': 'MA', 'pa.': 'PA', 'sd': 'SD'}


def build_sentiment(sent_fp):
    result = defaultdict(float)
    for line in sent_fp:
        parts = line.decode("utf-8").split("\t")
        result[parts[0]] = float(parts[1])
    return result

def get_state_from_tweet(tweet_json):
    # Check user's place
    place = None
    if "user" in tweet_json and "location" in tweet_json["user"]:
        place = tweet_json["user"]["location"]
    if place is None and "place" in tweet_json:
        place = tweet_json["place"]
    if place is not None:
        place = place.lower()
        for state_str in STATE_NAMES.keys():
            if state_str in place.split():
                return STATE_NAMES[state_str]
    else:
        return None

def handle_tweets(tweet_fp, sentiment):
    state_sentiment_observations = defaultdict(list)
    for line in tweet_fp:
        tweet_json = json.loads(line)
        if "text" not in tweet_json:
            # Could be a delete.
            continue
        state = get_state_from_tweet(tweet_json)
        if state is None:
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
            # We have a sentiment score for this tweet, register this as a sentiment observation for the state
            state_sentiment_observations[state].append(total)

    # Ok, we've gone through all the tweets. Average each word sentiment and print it.
    best_state = ""
    best_score = -1000000
    for s, l in state_sentiment_observations.iteritems():
        avg = sum(l) / len(l)
        if avg > best_score:
            best_state = s
            best_score = avg
    print best_state.encode("utf-8")

def main():
    sent_file = open(sys.argv[1])
    sentiment = build_sentiment(sent_file)
    sent_file.close()
    tweet_file = open(sys.argv[2])
    handle_tweets(tweet_file, sentiment)
    tweet_file.close()

if __name__ == '__main__':
    main()
