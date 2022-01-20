from imdb import IMDb
import csv
from py2neo import Graph
import re

user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

g = Graph(host=host, user=user, password=pwd)

movies= g.run("MATCH (n:MOVIE) RETURN n.imdbID")

movieIDs= []
for movie in movies:
    movieIDs.append(movie[0])

# create an instance of the IMDb class
ia = IMDb()

with open('IMDB/TitleBasics.tsv', encoding='utf-8') as csv_file:
    examples= []
    csv_reader = csv.reader(csv_file, delimiter='\t')
    nRow= 1
    for row in csv_reader:
        if nRow == 1:
            fields= (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        else:
            if not row[0] in movieIDs:
                query = "CREATE (n:MOVIE:" + row[1].upper()
                if row[4] == 1:
                    query+= ":ADULT"
                if row[8] != "\\N":
                    for genre in row[8].split(","):
                        query+= ":" + re.sub("\W", "", genre.upper())
                query+= " {imdbID: '%s', primaryTitle: '%s', originalTitle: '%s'" % (row[0], row[2].replace("'", "\\'"), row[3].replace("'", "\\'"))
                if row[5] != "\\N":
                    query+= ", startYear: '%s'" % (row[5])
                if row[6] != "\\N":
                    query+= ", endYear: '%s'" % (row[6])
                if row[7] != "\\N":
                    query+= ", runtimeMinutes: '%s'" % (row[7])
                query+= "})"

                g.run(query)
        nRow+= 1
        continue