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

# tokenizes the specific tweet to pull out names
# input: document -> single tweet
# output: sentence -> tokenized tweet
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
    return tweet

# lets make a function that takes in a set of tweets and applies a regular expression
# simple helper function
# input: tweets -> set of all tweets, regex -> regular expression
# output: bool -> true if regex was matched, false otherwise
def tweetFilter(tweet, regex):
    tweet_text = removePunc(tweet)
    #tweet_text = tweet['text']
    match = re.search(regex, tweet_text)
    if match != None:
        return True
    else:
        return False

# helper function to get only nominated tweets
# input: tweets -> set of all tweets
# output: nom_tweets -> set of tweets with a form of nominate within
def get_nom_tweets(tweets, award_list):
    # nomination regex
    regex = re.compile(r"nomin((?:(?:at(?:ed|ion)))|ee)")
    # blacklist regex
    regex_blacklist = re.compile(r"no.+nomin((?:(?:at(?:ed|ion)))|ee)")

    nom_tweets = []
    for tweet in tweets:
        tweet_text = tweet["text"]
        if tweetFilter(tweet_text, regex) and not tweetFilter(tweet_text, regex_blacklist):
            #this means we matched out regex and did not match our blacklist
            for award_name in award_list:
                if award_name in tweet_text.lower():
                    nom_tweets.append(tweet_text)
    return nom_tweets

    '''
    print("Length Before: " + str(len(nom_tweets)))
    for tweet in nom_tweets:
        print(tweet)
        tweet_low = tweet.lower()
        # loop through possible names for individual award
        for award_name in award_list:
            # remove tweet from list if there is no award name match
            if award_name not in tweet_low:
                print(tweet)
                nom_tweets.remove(tweet)
    print("Length After: " + str(len(nom_tweets)))
    '''
    return nom_tweets
    

# helper function to pull out all the named entities in a tweet
# input: tweet -> single tweet string
# output: name_list -> list of PERSON tagged chunks
def checkNames(tweet):
    name_list = []
    #print("Full list: " + str(name_list))
    #tokenize tweet
    tokens = nltk.word_tokenize(tweet)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.ne_chunk(tagged)

    #print(entities)
    # loop through chunks to find the person    
    for chunk in entities:
        #only look at the trees
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                name_string = ""
                for element in chunk:
                    name_string += element[0] 
                name_list.append(name_string)

        #print(nom_list)
    return name_list

# function to create tweet dictionary (lets just get some names)
def buildTweetDict(tweet_set):
    full_name_list = []
    
    for tweet in tweet_set:
        # check if the name list is empty
        full_name_list += checkNames(tweet)
        print("DONE WITH ITER")

    print(full_name_list)
    return full_name_list

def testForAward(tweets):
    # dif names for same award (hardcoded)
    pass    

if __name__ == '__main__': 

    award_name_list = ["best actress drama", "best drama actress", "motion picture drama", "best actress"]

    tweet_data = loadjson()
    nom_tweets = get_nom_tweets(tweet_data, award_name_list)
    #print(nom_tweets)
    nom_list = buildTweetDict(nom_tweets)
    #print(nom_list)
    #print(tweet_dict)
    #print(r)



    #tweet = "Brad Pitt wins best actor!67"
    #s = tokenize_preprocess(tweet)
    #s2 = removePunc(tweet)
    #print(s2)
