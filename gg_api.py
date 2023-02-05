'''Version 0.35'''
import json
import csv
import re
from nominees import *

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

def loadIMDb():
    pass

#OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
#OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

class Award:
    #initialize award
    def __init__(self, name, nominees):
        #Hard coded for now
        #we should mane the name category a list of possible names
        #for example Best Actress - Motion Picture - Drama would be:
        # [best actress drama, best drama actress, best actress motion picture drama]
        
        self.names = name
        self.Nominee = nominees
        self.winner = ""
        self.presenters = ""

    def checkWinner(self):
        #Type check for if winner is in our list of nominees
        if self.winner in self.nominees:
            #this means that we have found a winner in our list of nominees
            return True
        else:
            return False

tweets = ["Argo wins Best Picture", "argo wins Best Motion Picture - Drama", "Django Unchained is Tarantino's best movie", "And the Award for best picture drama goes to Argo", "Zero Dark should've won Best Motion Picture - drama", "Argo win best picture award"]

def buildRegexWins(award, element):
    # function builds out our regular expressions
    # i think there is a better way to do this

    reg_ex_list = []
    reg1 = r""+ element[0] + r".+" + award.name
    reg2 = r".+(award).+(" + element[0] + r")"
    reg3 = r"("+ element[0] + r")\s(wins?).+"
    
    reg_ex_list.append(reg1)
    reg_ex_list.append(reg2)
    reg_ex_list.append(reg3)
    return reg_ex_list

def buildRegexAward():
    reg_ex_list = []
    #reg1 = r".+(best actress).+(nominated?).+"
    #reg1 = r".+(wins best ).+(-).+$"
    reg2 = r".+ (best).+"
    #reg3 = r".+ (nominated for) .+"
    reg3 = r".+ (award) .+"
    reg4 = r".+ w((?:(?:in(?:ner)|on))|ins?) .+"
    reg5 = r".+ nomin((?:(?:at(?:ed)|ion))|ee|ees?) .+"
    #reg6 = r".+
    
    #reg2 = r".+(nominated?)\s(for)\s(best actress).+"

    #Hard coding for best actress
    #reg3 = r".+(best actress).+(nominees?).+"

    #reg_ex_list.append(reg1)
    reg_ex_list.append(reg2)
    reg_ex_list.append(reg3)
    reg_ex_list.append(reg4)
    reg_ex_list.append(reg5)
    
    return reg_ex_list

def buildNominees(award, tweet_data):
    winning_tweets = []
    for tweet in tweet_data:
        text = tweet['text']
        for name in award.names:
            #reg_list = buildRegexNom(award, name)
            reg_list = buildRegexAward()
            for reg in reg_list:
                result = re.search(reg, text, re.IGNORECASE)
                if result != None:
                    #print("Tweet: " + text)
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
        text = tweet['text']
        for element in award.Nominee:
            reg_list = buildRegexWins(award, element)
            
            for reg in reg_list:
                result = re.search(reg, text, re.IGNORECASE)
                
                # check if match exists
                if result != None:
                    print("Tweet: " + text)
                    winning_tweets.append(text)
                    element[1] += 1
                    
    # return list of winning tweets for visualization
    return winning_tweets

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(award):
    winner = ["", 0]
    for cand in award.Nominee:
        print(cand)
        if cand[1] > winner[1]:
            print("new winner")
            winner = cand
    if winner[0] != "":
        award.winner = winner[0]
    else:
        return "inconclusive"


def potenchAwards(tweets):
    maybeAward = []
    #patterns = [r'best+(\b\w.+)+(?= at| for)']
    #patterns = [r'(w((?:in(?:ner)|on))|ins?)+\s(\b\w.+)+(?= at| for| in| http)']
    #patterns = [r'best.+(?= at| for| in| http| \B#)']
    #patterns = [r'best.+(?= for)', r'best.+\B#', r'best.+(?= at)']

    #pattern1 =  [r'won\s+(\b\w.+)+(?= at| for)', r'wins\s+(\b\w.+)+(?= http)', r'won\s+(\b\w.+)+(?= http)', r'wins\s+(\b\w.+)+\B.', r'for\s+(\b\w.+)+(goes to).+\B.', r'won\s+(\b\w.+)+\B.', r'for\s+(\b\w.+)+(goes to).+\B#', r'(nominated for)\s+(\b\w.+)+(?= at| for)']
    
        #in this iteration, refine to most specific 
    #for tweet in tweets:
        #tweet = tweet.lower()
       # for pattern in patterns:
            #matches = re.findall(pattern, tweet)
            #for award in matches:
               # maybeAward.append(award)
    pattern = re.compile("Best ([A-z\s-]+)[A-Z][a-z]*[^A-z]")
    maybeAward = [pattern.search(tweet).group(0)[:-1] for tweet in tweets if pattern.search(tweet)]
    #pattern1 = re.compile(".*^((?!(goes|was|award|win| is| to)).)*$")
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

    #pattern2 = re.compile('.+(?= at)')
    #huh = [pattern2.match(tweet).group(0) for tweet in huh if pattern2.match(tweet)]
    
        

                    #words = award.split()
                    #if ("for" or "in" or "at" or "#" or "http") in words:
                        #awd = words[:words.index()]
                        #maybeAward.append(words[:words.index("for")])
                    #else:
                       #maybeAward.append(award)
    
    #phrase_counts = dict(Counter(maybeAward))

    phrase_counts = dict(Counter(huh))
    award_list = dict(sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True))
    awdls2 = []
    for awd in award_list:
        if phrase_counts[awd] > 1:
            awdls2.append(awd)

    return awdls2     

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def humanReadable(awards):
    for award in awards:
        print("Award:", award.name, "\nPresenters:", award.presenter, "\nNominees: ", award.Nominee, "\nWeiner: ", award.winner, "\n\n")
    
def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # this function loads in our twitter database and stores it in variable
    print('START OF CODE')
    tweet_data = loadjson()
    hard_code_nom = [["Argo", 0], ["Django Unchained", 0], ["Life of Pi", 0], ["Lincoln", 0], ["Zero Dark Thirty", 0]]
    golden_globes = Award("Best Actress", hard_code_nom)

    hard_code_nom2 = [["Jessica Chastain", 0], ["Marion Cotillard", 0], ["Helen Mirren", 0], ["Naomi Watts", 0], ["Rachel Weisz", 0]]
    hc_award_names = ["Best Actress Drama", "Best Drama Actress", "Best Actress Motion Picture Drama", "Best Actress - Motion Picture - Drama"]
    
    golden_globes2 = Award(hc_award_names, hard_code_nom2)
    
    #winner = buildConfidence(golden_globes2, tweet_data)
    #print(winner)
    #get_winner(golden_globes2)

    #print("Winner: " + golden_globes2.winner)
    winning_noms = buildNominees(golden_globes2, tweet_data)
    print(len(winning_noms))
    print("BARRIER")
    for tweet in winning_noms[:6500]:
        result = re.search(r"^(?!.*TV).*(drama).*$", tweet, re.IGNORECASE)
        if result != None:
            print("Tweet: " + tweet)


    phrase_counts = potenchAwards(winning_noms)
    print("Phrase Counts: ", phrase_counts)

    awards = []
    for awd in phrase_counts:
        award = Award(awd, None)
        awards.append(award)

    with open("Data/output.json", "w") as file:
        json.dump(awards, file)

    return

if __name__ == '__main__':
    main()
