# CS337 Project 1: Twitter
Golden Globe Project Master

Project 1: Twitter [Sofia Vergara’s ( . )( . )]
Dataset: given set of tweets gg2013.json

Output Requirements:
Winners, given nominees and award names
Winners, given only award names
Nominees, given award names
Award names (given only the name of the award ceremony)
Award presenter(s), given award names
host(s) (given name of award ceremony)
Needs to run in under 10 mins

Initial Framework (What we need to do):
Mine / build type constraints (person, or actor) and implement type-checking to use these as filters.
Two broad categories (type of Awards, Nominees)
Need type constraints
Used when parsing through tweets to constrain what we are getting out. For example when we just want the Award we want to constrain the string as to only pick out said award.
Ordering constraints
Essentially we are building the tools to comb tweets
Build regular expressions/ keyword methods for initial extraction.
Find and clean IMDb dataset
Iter1: Pull list of awards and nominees, check names against this list
Iter2: Using name of awards, match awards to names to generate a list of nominees, once we build these lists, go back and comb for winners (essentially what Iter1 does once list of nominees is generated)
IterF: comb for award names, once that is finalized then go into Iter2
Main data extraction from Twitter database
Build regular expressions
Getting rid of “my prediction” type of tweet
Either gonna find a package that throws away non-factual statements, or just have to throw away anything deemed “non-basic”
Throw away stuff that doesnt have to do with anything
Toss anything not speaking American
Look for terms like “win” “champ” etc. (need to come up with list later)
Get rid of anything with another award or event (ex. Oscar)
Anything that doesnt meet regex pattern recognition that we will define to look for
Nominee, verb, award
Timestamp check, get rid of anything before award ceremony (temporal parsing) (ONLY WHEN LOOKING FOR WINNERS)
Potential: If 100 people say Brad Pitt won and one guy said something else, do we trash anything else tweeted by that guy
Potential: If a nominee is up for multiple awards and there is a tweet not specifying what award they won, trash it
Potential: If this runs slowly, do an initial comb before anything to get rid of boob tweets before even attempting anything
Apply type checks and relational constraints (you have to be nominated to win).  Might do this before
Phrasal parsing here to ensure the tweet is saying the right thing
Doing this before clustering so we do not have to cluster unnecessary info
Temporal constraints, look at the times of the tweets for winners
Cluster results (full names vs. only first or last, truncated names of awards, etc. (clean happens before this, then this becomes a parse and pull)


Aggregation / voting.  More sophisticated approaches might weight the voting based on confidence in the extractions.
Possibly throwing out tweets that are “trolling” or vague


Scrub data for important words (aka throw out anything jargon)
Building regular expressions to extract needed information
Find and scrub IMDb dataset of actors and directors
Start with the easiest case (Number 1: Winners, given nominees and award names)
Build some sort of structure to store our variables?


Run Time Structure
Extraction
Apply constraints
Clustering 
Aggregation 

Needed Packages / Good Links:
NLTk
spaCy
Re: regular expression operations (https://docs.python.org/3/library/re.html) 
IMDb dataset: https://www.imdb.com/interfaces/
Possible python packages: https://www.upgrad.com/blog/python-nlp-libraries-and-applications/
Imdb movie database api: https://rapidapi.com/blog/how-to-use-imdb-api/ 


For IMDb datasets:
name.basics.tsv.gc
Names (directors, actors)
Movies they are known for
