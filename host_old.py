import json
import nltk
import re
import en_core_web_sm
import string

stop_words = nltk.corpus.stopwords.words('english')
stop_words += ["RT" + "congrats" + "woah" + "wow"]
award_stop_words = ["better", "globe", "directora", "oscars", "oscar", "best", "picture", "motion", "drama", "golden", "globes", "goldenglobes", "actor", "actress", "musical", "comedy", "supporting", "director", "screenplay", "animated", "film", "films", "feature", "movie"]


def loadjson(file):
    #Load in JSON
    #JSON Structure:
    # { "text": whatever the text of the tweet holds
    #   "user": {screen name, user id}
    #   "id": tweet id
    #   "timestamp_ms": time of tweet (Long float structure)
    # }
    with open(file, "r") as fp:
        data = json.load(fp)
    return data

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

# lets make a function that takes in a set of tweets and applies a regular expression
# simple helper function
# input: tweets -> set of all tweets, regex -> regular expression
# output: bool -> true if regex was matched, false otherwise
def tweetFilter(tweet, regex):
    match = re.search(regex, tweet.lower())
    if match != None:
        return True
    else:
        return False

# helper function to get only nominated tweets for specific award
# input: tweets -> set of all tweets
# output: nom_tweets -> set of tweets with a form of nominate within
def get_host_tweets(tweets):
    regex_list = [
        r"(hosts?|hosting)"
    ]

    nom_tweets = []
    for tweet in tweets:
        for reg_exp in regex_list:
            regex = re.compile(reg_exp)
            #print("REGEX: " + reg_exp)
            if tweetFilter(tweet, regex):
                #this means we matched our regex
                nom_tweets.append(tweet)
                break
    return nom_tweets
    

# helper function to pull out all the named entities in a tweet
# input: tweet -> single tweet string
# output: name_list -> list of PERSON tagged chunks
def checkNames(tweet):
    # make sure that the PERSON is also a proper noun

    name_list = []
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
                for leaf in chunk.leaves():
                    if leaf[0].lower() not in award_stop_words and leaf[1] == "NNP":

                        name_string += leaf[0] + " "
                if name_string != "":
                    name_list.append(name_string)

    return name_list

# function to create tweet dictionary (lets just get some names)
def buildNameList(tweet_set):
    full_name_list = []
    for tweet in tweet_set:
        # check if the name list is empty
        full_name_list += checkNames(tweet)

    #print(full_name_list)
    return full_name_list

def countNames(name_list):
    full_count_dict = {}
    #put first element into count list

    for name in name_list:
        full_count_dict[name] = full_count_dict.get(name, 0) + 1

    return full_count_dict


#award example: best director motion picture
#desired outomce: ["best director motion picture", "best director motion", "best director"]
# award is inputed as a string
def getHost():
    cleaned_tweet_data = loadjson("Data/cleaned_tweets.txt")

    host_tweets = get_host_tweets(cleaned_tweet_data)
    name_list = buildNameList(host_tweets)
    names_dict = countNames(name_list)
    sorted_list = sorted(names_dict.items(), key = lambda kv: kv[1])
    
    final_list = []
    for element in sorted_list[-2:]:
        final_list.append(element[0])
    
    hosts = final_list
    return hosts