import urllib
import json

for i in range(10):
    response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft&page=" + str(i+1))
    j = json.load(response)
    for r in j["results"]:
        print r["text"]

