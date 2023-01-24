# fucking around with regex
import re

# pontential tweets
# "[Brad Pitt] won [Best Actor for real!]"
# "[And the] Award [for Best Actor] goes to [Brad Pitt]"
# "[Brad Pitt is the] winner [of Best Actor]"

tweets = ["Brad Pitt wins Best Actor", "Micheal Bay wins best director", "Brad Pitt is such a stupid guy", "And the Award for best actor goes to Brad Pitt"]

regular_expression_list = [r'[^a-zA-Z]wins[^a-zA-Z]', r'[^a-zA-Z][aA]ward[^a-zA-Z]goes to[^a-zA-Z]']


kept_tweets = []
for tweet in tweets:
    for reg in regular_expression_list:
        result = re.search(reg, tweet)
        if result != None:
            #this means we have passed one of our regular expressions so we keep this tweet
            kept_tweets.append(tweet)
            break
        else:
            print("Tweet thrown out")

print(kept_tweets)

#string = "Brad Pitt wins Best Actor"
#results = re.search(r'[^a-zA-Z]wins[^a-zA-Z]', string)
#print(results.group())

#Start with a tweet
#check it against our family of regular expressions
# if they are all NoneTypes then this tweet is irrelevant
# Simple "WINS" Regex: r'[^a-zA-Z]wins[^a-zA-Z]'
# Checks for any character at the beggining or end of string with "wins" in the middle