'''Version 0.35'''
import json
import csv
import re

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
        
        self.name = name
        self.Nominee = nominees
        self.winner = ""

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

def buildRegexNom(award):
    reg_ex_list = []
    #reg1 = r".+(nominated?).+"
    #reg2 = r".+(nominated?)\s(for)\s(" + award.name +").+"
    reg3 = r".+(nominees?).+"

    #reg_ex_list.append(reg1)
    reg_ex_list.append(reg3)
    return reg_ex_list

def buildNominees(award, tweet_data):
    winning_tweets = []
    for tweet in tweet_data:
        text = tweet['text']
        reg_list = buildRegexNom(award)
        for reg in reg_list:
            result = re.search(reg, text, re.IGNORECASE)
            if result != None:
                print("Tweet: " + text)
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
        

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

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
    golden_globes2 = Award("Best Actress - Motion Picture - Drama", hard_code_nom2)
    
    #winner = buildConfidence(golden_globes2, tweet_data)
    #print(winner)
    #get_winner(golden_globes2)

    #print("Winner: " + golden_globes2.winner)
    winning_noms = buildNominees(golden_globes, tweet_data)
    #print(winning_noms)
    return

if __name__ == '__main__':
    main()
