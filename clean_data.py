# this file is just to output cleaned tweet data
# essentially for quicker runtime in testing

import json
import nltk
import re
import string

stop_words = nltk.corpus.stopwords.words('english')
stop_words += ["rt", "congrats", "congratulations", "woah", "wow", "woo"]

#Initial Python File
def loadjson(year):
    #Load in JSON
    #JSON Structure:
    # { "text": whatever the text of the tweet holds
    #   "user": {screen name, user id}
    #   "id": tweet id
    #   "timestamp_ms": time of tweet (Long float structure)
    # }

    file = open("Data/gg%s.json" %year)
    data = json.load(file)

    return data

# helper function to remove all links from tweets
def removeLink(tweet_text):
    regex = re.compile(r"((https?):((//)|(\\\\)).+((#!)?)*)")
    links = re.findall(regex, tweet_text)
    for url in links:
        tweet_text = tweet_text.replace(url[0], ', ')
    return tweet_text

# helper function to remove usernames and hashtags, along with punctuation
def removeTags(tweet_text):
    prefix = ['@', '#']
    for sep in string.punctuation:
        if sep not in prefix:
            tweet_text = tweet_text.replace(sep, ' ')
    word_list = []
    for word in tweet_text.split():
        word = word.strip()
        if word:
            if word[0] not in prefix:
                word_list.append(word)
    return ' '.join(word_list)

# this is a helper function to clean the tweet data
# it strips punctuation along with removing stopwords
def cleanTweets(tweet_data):
    #print(stop_words)
    filteredTweets = []
    for tweet in tweet_data:
        temp_tweet = removeLink(tweet['text'])
        temp_tweet = removeTags(temp_tweet)

        words = nltk.word_tokenize(temp_tweet)
        wordsFiltered = []
        for w in words:
            if w.lower() not in stop_words:
                wordsFiltered.append(w)
        new_string = ' '.join(map(str, wordsFiltered))
        #print("Stop Words Removed: " + new_string + "\n")
        filteredTweets.append(new_string)
    return filteredTweets

def dumpJSON(tweet_list, year):
    file_name = 'Data/cleaned_tweets%s.txt' %year
    with open(file_name, 'w') as f:
        json.dump(tweet_list, f)
    print("DONE CLEANING")
    return file_name

def full_clean(year):
    print("CLEANING TWEETS")
    tweet_data = loadjson(year)
    return dumpJSON(cleanTweets(tweet_data), year)
