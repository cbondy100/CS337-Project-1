#Will get all the nominees for a given award
# will need a different classifyer for movie awards than people awards
# from the set of tweets build a stopword list based on the awards and ceremony
# write some more regular expressions to improve our nomination tweet set

import json
import nltk
import re
import en_core_web_sm
import string

#nlp = en_core_web_sm.load()

stop_words = nltk.corpus.stopwords.words('english')
stop_words += ["RT"]
award_stop_words = ["globe", "directora", "oscars", "oscar", "best", "picture", "motion", "drama", "golden", "globes", "goldenglobes", "actor", "actress", "musical", "comedy", "supporting", "director", "screenplay", "animated", "film", "films", "feature", "movie"]

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
best_drama_names = ["best picture", "best drama", "best picture drama", "picture drama", "drama", "best picture - drama"]
best_anim_names = ["best picture - animated", "animated", "best animation", "best pictured animated", "best animated picture", "best animated film", "film animated"]
best_director = ["best director - motion picture", "best director motion", "best director", "director"]
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
    chars = "!$%&()*+,-./:;<=>?@[\]^_`{'~}"
    chars += '"1234567890'
    for c in chars:
        tweet = tweet.replace(c, '')
    return tweet

# lets make a function that takes in a set of tweets and applies a regular expression
# simple helper function
# input: tweets -> set of all tweets, regex -> regular expression
# output: bool -> true if regex was matched, false otherwise
def tweetFilter(tweet, regex):
    #tweet_text = tweet['text']
    match = re.search(regex, tweet)
    if match != None:
        return True
    else:
        return False

# helper function to get only nominated tweets
# input: tweets -> set of all tweets
# output: nom_tweets -> set of tweets with a form of nominate within
def get_nom_tweets(tweets):
    # nomination regex
    # gotta build some more regular expressions
    # Nomination alt text: (deserved to win) (should have won) (wins over) (just beat) (wanted _ to win)
    #Hotel Transylvania is nominated for Two golden globes tonight \"Best Animated Film\" and \" Outstanding Animation in an Animated Feature Film\""
    regex = re.compile(r"nomin((?:(?:at(?:ed|ion)))|ee)")
    # blacklist regex
    #regex_blacklist = re.compile(r"no.+nomin((?:(?:at(?:ed|ion)))|ee)")

    nom_tweets = []
    for tweet in tweets:
        if tweetFilter(tweet, regex):
            #this means we matched out regex
            for award in best_director:
                if award.lower() in tweet.lower():
                    nom_tweets.append(tweet)
    return nom_tweets
    

# helper function to pull out all the named entities in a tweet
# input: tweet -> single tweet string
# output: name_list -> list of PERSON tagged chunks
def checkNames(tweet):
    # make sure that the PERSON is also a proper noun

    name_list = []
    #print("Full tweet: " + tweet)
    #tokenize tweet
    tokens = nltk.word_tokenize(tweet)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.ne_chunk(tagged)
    # loop through chunks to find the person    
    for chunk in entities:
        #print(chunk)
        #print('CHUNK: ' + str(chunk))
        #only look at the trees
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                name_string = ""
                for leaf in chunk.leaves():
                    if leaf[0].lower() not in award_stop_words and leaf[1] == "NNP":
                        #print("LEAF:" + str(leaf))
                        #print(leaf[0] + " added to name_list")
                        name_string += leaf[0] + " "
                if name_string != "":
                    name_list.append(name_string)
        #print("\n")
        #print(nom_list)
    #print(name_list)
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
    filteredTweets = []
    get_substring = lambda s: s.split("RT @")[0] + s.split(": ")[-1]
    for tweet in tweet_data:
        #print("Original Tweet: " + tweet['text'])
        temp_tweet = removeLink(tweet['text'])
        #print("Link Removed: " + temp_tweet)
        temp_tweet = removeTags(temp_tweet)
        #print("Tags removed: " + temp_tweet)

        words = nltk.word_tokenize(temp_tweet)
        wordsFiltered = []
        for w in words:
            if w not in stop_words:
                wordsFiltered.append(w)
        new_string = ' '.join(map(str, wordsFiltered))
        #print("Stop Words Removed: " + new_string + "\n")
        filteredTweets.append(new_string)
    return filteredTweets

def testForAward(tweets):
    # dif names for same award (hardcoded)
    pass    

if __name__ == '__main__': 

    # From this awards list we would like to extract:
    # Jessica Chastain, Marion Cotillard, Helen Mirren, Naomi Watts, Rachel Weisz

    #@glasneronfilm @ZulekhaNathoo Best Actress-Drama, I'm calling Naomi Watts.  Best Actress-Musical/Comedy, Jennifer Lawrence. #goldenglobes
    #RETWEET if you think she deserves to win for her performance in #TheImpossible.
    #"THE D IS SILENT" - nominee Marion Cotillard, seconds before flipping a table at the #goldenglobes

    #sample_tweet_data = ["RT @ BrookeAnderson : Ang Lee , nominated Best Director work @ LifeofPiMovie", "Ben affleck nominated for Best Director"]

    tweet_data = loadjson()
    cleaned_data = cleanTweets(tweet_data)

    #for tweet in cleaned_data:
    #    if "Ang Lee" in tweet:
    #        print("FOUND ANG LEE IN CLEANED DATA")
    #        print(tweet)
    nom_tweets = get_nom_tweets(cleaned_data)
    #print(nom_tweets)
    name_list = buildNameList(nom_tweets)
    print(name_list)
    #countNames(name_list)

    '''
    for tweet in tweet_data:
       tweet_text = tweet['text']
       if tweetFilter(tweet_text, r"(Argo)"):
        print(tweet_text)
    '''
    #string = 
    #get_substring = lambda s: s.split("@")[0] + s.split(":")[-1]
    #print(get_substring(string))
    #"RT @ BrookeAnderson : Ang Lee , nominated Best Director work @ LifeofPiMovie"