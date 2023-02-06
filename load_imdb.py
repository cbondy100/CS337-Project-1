# load imdb dataset
import csv
import json

def load_in():
    actor_list = []

    with open("Data/name.basics.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        for line in tsv_file:
            actor_list.append(line[1])


    with open('Data/actor_list.txt', 'w') as f:
        json.dump(actor_list, f)
