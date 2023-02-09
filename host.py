import nltk
import json
import re

host_ignore_words = ["host", "hosts", "hosting", "year" "next"]
host_stop_words = ["next", "year"]

#Initial Python File
def loadjson(year):
    #Load in JSON
    #JSON Structure:
    # { "text": whatever the text of the tweet holds
    #   "user": {screen name, user id}
    #   "id": tweet id
    #   "timestamp_ms": time of tweet (Long float structure)
    # }
    with open("Data/cleaned_tweets%s.txt" %year, "r") as fp:
        data = json.load(fp)
    return data

def countEntities(list):
    full_count_dict = {}
    
    for entity in list:
        full_count_dict[entity] = full_count_dict.get(entity, 0) + 1
    return full_count_dict

def getHostTweets(tweets):
    regex = r"([Hh]osts?|[Hh]osting)"
    host_tweets_words = []
    for tweet in tweets:
        #tweet = tweet.lower()
        if re.search(regex, tweet) != None:
            for w in host_stop_words:
                if w not in tweet:
                    words = tweet.split()
                    pairs = [words[i]+' '+words[i+1] for i in range(len(words)-1)]
                    host_tweets_words += pairs

    return host_tweets_words

def getFinalHost(year):
    tweets = loadjson(year)
    host_words = getHostTweets(tweets)
    #print(host_words)
    counts = countEntities(host_words)
    counts = sorted(counts.items(), key = lambda kv: kv[1])

    final_list = []
    for element in counts[-2:]:
        final_list.append(element[0])

    return final_list

if __name__ == "__main__":
    print(getFinalHost())