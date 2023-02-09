'''Version 0.35'''
import json
import csv
import re
from nominees import *
from clean_data import *
from collections import Counter
from presenters import *
from host import *

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

#OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
#OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

class Award:
    #initialize award
    def __init__(self, name):
        
        self.names = name
        self.Nominee = []
        self.winner = ""
        self.presenters = ""

    def checkWinner(self):
        #Type check for if winner is in our list of nominees
        if self.winner in self.nominees:
            #this means that we have found a winner in our list of nominees
            return True
        else:
            return False
        
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    print("GETTING HOST")
    hosts = getFinalHost(year)

    return hosts

def get_awards(award_list):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = []
    for award in award_list:
        awards.append(award.names)
    return awards

def get_nominees(award_list):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    nominees = {}
    for award in award_list:
        nom_list = []
        for nominee in award.Nominee:
            nom_list.append(nominee[0])
        nominees[award.names] = nom_list
    return nominees

def get_winner(award):
    winner = ["", 0]
    for cand in award.Nominee:
        if cand[1] > winner[1]:
            winner = cand
    if winner[0] != "":
        award.winner = winner[0]
    else:
        return "inconclusive"

def get_presenters(award_list):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    presenters = {}
    for award in award_list:
        prez_list = []
        for prez in award.presenters:
            prez_list.append(prez)
        presenters[award.names] = prez_list
    return presenters
   
def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    #this is where we should clean our tweets and load in our IMDB Dataset
    full_clean("2013")
    global tweet_data 
    tweet_data = loadjson("Data/gg2013.json") 

    return

def buildRegexWins(award, element):
    # function builds out our regular expressions
    # i think there is a better way to do this

    reg_ex_list = []
    reg1 = r""+ element[0] + r".+" + award.names
    reg2 = r".+(award).+(" + element[0] + r")"
    reg3 = r"("+ element[0] + r")\s(wins?).+"
    
    reg_ex_list.append(reg1)
    reg_ex_list.append(reg2)
    reg_ex_list.append(reg3)
    return reg_ex_list

def buildRegexAward():
    reg_ex_list = []
    reg2 = r".+ (best).+"
    reg3 = r".+ (award) .+"
    reg4 = r".+ w((?:(?:in(?:ner)|on))|ins?) .+"
    reg5 = r".+ nomin((?:(?:at(?:ed)|ion))|ee|ees?) .+"
    
    reg_ex_list.append(reg2)
    reg_ex_list.append(reg3)
    reg_ex_list.append(reg4)
    reg_ex_list.append(reg5)
    
    return reg_ex_list

def filterAwardTweets(tweet_data):
    winning_tweets = []
    for tweet in tweet_data:
        text = tweet['text']

        reg_list = buildRegexAward()
        for reg in reg_list:
            result = re.search(reg, text, re.IGNORECASE)
            if result != None:

                winning_tweets.append(text)

    return winning_tweets


def buildConfidence(award, tweet_data):
    # function builds out Nominees dictionary and adds
    # to the "confidence" score based on how many RegEx 
    # each nominee passes

    winning_tweets = []

    # go through each tweet and each nominee
    # match family of regular expressions
    for tweet in tweet_data:
        text = tweet
        for element in award.Nominee:
            reg_list = buildRegexWins(award, element)
            
            for reg in reg_list:
                result = re.search(reg, text, re.IGNORECASE)
                
                # check if match exists
                if result != None:
                    winning_tweets.append(text)
                    element[1] += 1
                    
    # return list of winning tweets for visualization
    return winning_tweets


'''
def dupAwards(awards_f, award):
    bool = False
    for aw in awards_f:
        if aw.names != award.names:
            if aw.Nominee != []:
                if aw.Nominee == award.Nominee:
                    bool = True
    return bool
'''
def dupAwards(awards_f, award):
    bool = False
    temp_l = []
    for nom in award.Nominee:
        temp_l.append(nom[0])
    for aw in awards_f:
        if aw.names != award.names:
            temp_i = []
            for nomm in aw.Nominee:
                temp_i.append(nomm[0])
            if sorted(temp_l) == sorted(temp_i):
                bool = True
                
    return bool

def buildNoms(awards):
    for award in awards:
        getFinalNoms(award, "2013")
        getFinalPres(award, "2013")
        if dupAwards(awards, award):
            awards.remove(award)
            print("POPPED: " + str(award))

    return awards

def potenchAwards(tweets):
    maybeAward = []
    pattern = re.compile("Best ([A-z\s-]+)[A-Z][a-z]*[^A-z]")
    maybeAward = [pattern.search(tweet).group(0)[:-1] for tweet in tweets if pattern.search(tweet)]

    pattern1 = re.compile(".*^((?!(goes|but|award|is|win)).)*$")
    maybeAward = [pattern1.match(tweet).group(0).lower() for tweet in maybeAward if pattern1.match(tweet)]

    pattern2 = re.compile('.+(?= for)')
    maybeAward = [pattern2.match(tweet).group(0) for tweet in maybeAward if pattern2.match(tweet)]
    huh = []
    for award in maybeAward:
        award = award.replace(' -', '')
        award = award.replace('-', '')
        words = len(award.split())
        if words > 2 and words < 10: 
            huh.append(award)


    phrase_counts = dict(Counter(huh))
    award_list = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
    awdls2 = []
    threshold = award_list[0][1] / 25
    awards = []

    for awd in award_list:
        if awd[1] > threshold:
            award = Award(awd[0])
            awards.append(award)

    return awards


def humanReadable(awards):
    print("Hosts: ", get_hosts())
    for award in awards:
        print("Award:", award.names, "\nPresenters:", award.presenters, "\nNominees: ", award.Nominee, "\nWinner: ", award.winner, "\n\n")
 

def get_nominees_list(nominee_list):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    nominees = []
    for nom in nominee_list:
        nominees.append(nom[0])
    return nominees

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # this function loads in our twitter database and stores it in variable
    pre_ceremony()
    global award_list 
    award_list = potenchAwards(filterAwardTweets(tweet_data))
    #print(award_list)
    buildNoms(award_list)
    
    output = {}
    output["Host: "] = get_hosts("2013")
    for award in award_list:
        output[award.names] = {
            "Presenters" : award.presenters,
            "Nominees" : get_nominees_list(award.Nominee),
            "Winner" : award.winner
        }

    
    with open("Data/output.json", "w") as file:
        json.dump(output, file)
    

    get_awards(award_list)
    get_nominees(award_list)
    get_hosts("2013")
    get_presenters(award_list)

    return

if __name__ == '__main__':
    main()
