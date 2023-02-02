#Will get all the nominees for a given award

import json
import nltk
import re
import en_core_web_sm

#nlp = en_core_web_sm.load()


#Initial Python File
def loadjson():
    #Load in JSON
    #JSON Structure:
    # { "text": whatever the text of the tweet holds
    #   "user": {screen name, user id}
    #   "id": tweet id
    #   "timestamp_ms": time of tweet (Long float structure)
    # }

    file = open("Data/gg2013.json")
    data = json.load(file)

    return data

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

#good regex: nomin((?:(?:at(?:ed|ion)))|ee)

def tokenize_preprocess(document):
    document = ' '.join([i for i in document.split()])
    sentence = nltk.sent_tokenize(document)
    sentence = [nltk.word_tokenize(sent) for sent in sentence]
    sentence = [nltk.pos_tag(sent) for sent in sentence]
    return sentence

# remove punctuation and lowercase the tweet
def removePunc(tweet):
    chars = "!#$%&()*+,-./:;<=>?@[\]^_`{'~}"
    chars += '"1234567890'
    for c in chars:
        tweet = tweet.replace(c, '')
    return tweet.lower()

# lets make a function that takes in a set of tweets and applies a regular expression
def tweetFilter(tweets, regex):
    tweet_list = []
    for tweet in tweets:
        #tweet_text = removePunc(tweet['text'])
        tweet_text = tweet['text']
        match = re.search(regex, tweet_text)
        if match != None:
            tweet_list.append(tweet_text)

    return tweet_list

def get_nom_tweets(tweets):
    regex = re.compile(r"nomin((?:(?:at(?:ed|ion)))|ee)")
    nom_tweets = tweetFilter(tweets, regex)
    return nom_tweets

def checkNames(tweets):
    for tweet in tweets:
        tokens = nltk.word_tokenize(tweet)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.ne_chunk(tagged)
        for chunk in entities:
            print(chunk)
        
        #print(tweet)
        #proc_tweet = nlp(tweet)
        #print(proc_tweet.ents)
        break

if __name__ == '__main__': 

    tweet_data = loadjson()
    nom_tweets = get_nom_tweets(tweet_data)
    checkNames(nom_tweets)
    #print(r)



    #tweet = "Brad Pitt wins best actor!67"
    #s = tokenize_preprocess(tweet)
    #s2 = removePunc(tweet)
    #print(s2)
