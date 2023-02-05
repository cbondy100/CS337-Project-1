#Will get all the nominees for a given award

import json
import nltk
import re
import en_core_web_sm
import jellyfish

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
        tweet_text = removePunc(tweet["text"])
        if tweetFilter(tweet_text, regex) and not tweetFilter(tweet_text, regex_blacklist):
            #this means we matched out regex and did not match our blacklist
            for award_name in award_list:
                if award_name in tweet_text.lower():
                    nom_tweets.append(tweet_text)
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
def buildNameList(tweet_set):
    full_name_list = []
    for tweet in tweet_set:
        #print(tweet)
        # check if the name list is empty
        full_name_list += checkNames(tweet)

    #print(full_name_list)
    return full_name_list

def countNames(name_list):
    #print(name_list)
    full_count_dict = {}

    #put first element into count list

    #print(name_list)
    # checks each name against our list of names
    
    for name in name_list:
        full_count_dict[name] = full_count_dict.get(name, 0) + 1
    '''
    for element in full_count_list:
        for name in name_list:
            print(element[0] + name)
            if name == element[0]:
                print("FOUND A MATCH: " + name)
                element[1] += 1
                print(full_count_list)
                
            else:
                print("ADD A NEW NOMINEE: " + name)
                full_count_list.append([name, 1])
                #name_list.remove(name)
                print(full_count_list)
    '''    

    print(full_count_dict)

def testForAward(tweets):
    # dif names for same award (hardcoded)
    pass    

if __name__ == '__main__': 

    award_name_list = ["best actor", "best actor drama", "best actor motion picture drama", "actor drama", "drama actor", "award"]
    # From this awards list we would like to extract:
    # Jessica Chastain, Marion Cotillard, Helen Mirren, Naomi Watts, Rachel Weisz

    #@glasneronfilm @ZulekhaNathoo Best Actress-Drama, I'm calling Naomi Watts.  Best Actress-Musical/Comedy, Jennifer Lawrence. #goldenglobes
    #RETWEET if you think she deserves to win for her performance in #TheImpossible.
    #"THE D IS SILENT" - nominee Marion Cotillard, seconds before flipping a table at the #goldenglobes

    tweet_data = loadjson()
    nom_tweets = get_nom_tweets(tweet_data, award_name_list)
    #print(nom_tweets)
    name_list = buildNameList(nom_tweets)
    countNames(name_list)
    
    print(jellyfish.jaro_distance(u"Lincoln", u"LincolnGoldenGlobes"))
    print(jellyfish.jaro_distance(u"Lincoln", u"LincolnMakes"))
    print(jellyfish.jaro_distance(u"Lincoln", u"Wow"))
    print(jellyfish.jaro_distance(u"Lincoln", u"Argo"))

    '''
    for tweet in tweet_data:
       tweet_text = tweet['text']
       if tweetFilter(tweet_text, r"([Jj]oaquin)"):
        print(tweet_text)
    '''
    