import csv
from py2neo import Graph

user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

g = Graph(host=host, user=user, password=pwd)

g.run("MATCH(n:PERSON) DETACH DELETE n")

with open('IMDB/NamesBasics.tsv', encoding='utf-8') as csv_file:
    examples= []
    csv_reader = csv.reader(csv_file, delimiter='\t')
    nRow= 1
    for row in csv_reader:
        if nRow == 1:
            fields= (row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            query = "CREATE (n:PERSON {imdbID: '%s', primaryName: '%s'" % (row[0], row[1].replace("'", "\\'"))
            if row[2]!= "\\N":
                query+= ", birthYear: '%s'" % (row[2])
            if row[3] != "\\N":
                query+= ", deathYear: '%s'" % (row[3])
            query+= "})"
            g.run(query)
        nRow+= 1