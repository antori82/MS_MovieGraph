#This script processes IMDB tsv files and prepares them for import in Neo4j

import os

path= "./IMDB/"

with os.scandir(path) as it:
    for entry in it:
        if entry.name.endswith(".tsv") and entry.is_file():
            text = open(path + entry.name, "r", encoding='utf-8')
            text = ''.join([i for i in text]).replace('"', "")
            x = open(path + entry.name + "_proc.tsv","w", encoding='utf-8')
            x.writelines(text)
            x.close()