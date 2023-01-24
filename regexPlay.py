# fucking around with regex
import re

# pontential tweets
# "[Brad Pitt] won [Best Actor for real!]"
# "[And the] Award [for Best Actor] goes to [Brad Pitt]"
# "[Brad Pitt is the] winner [of Best Actor]"

tweets = ["Brad Pitt wins Best Actor", "Micheal Bay wins best director", "Brad Pitt is such a stupid guy", "Callum Bondy wins Best Coder"]

string = "Brad Pitt is the Best Actor"
results = re.search(r'[^a-zA-Z]wins[^a-zA-Z]', string)
print(results.group())

#Start with a tweet
#check it against our family of regular expressions
# if they are all NoneTypes then this tweet is irrelevant
# Simple "WINS" Regex: r'[^a-zA-Z]wins[^a-zA-Z]'
# Checks for any character at the beggining or end of string with "wins" in the middle