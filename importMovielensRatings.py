import csv
from py2neo import Graph

#Movielens data must be merged in a single table before Neo4j import. Specify the absolute path of the file you want to generate here.
path= "ABSOLUTE_PATH_TO_MERGED_FILE"

ids= {}
with open("Movielens/links.csv", "r") as linksFile:
    reader = csv.reader(linksFile)
    headers = next(reader, None)
    for row in reader:
        ids[row[0]]= "tt" + row[1]

with open("Movielens/ratings.csv", "r") as ratingsFile:
    reader = csv.reader(ratingsFile)
    headers = next(reader, None)
    with open(path, "w", newline='') as outFile:
        writer= csv.writer(outFile, delimiter= ",", )
        writer. writerow(headers)
        for row in reader:
            writer.writerow([row[0], ids[row[1]], row[2], row[3][:-1]])


user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

g = Graph(host=host, user=user, password=pwd)

g.run(""":auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///""" + path + """" AS row WITH row
MERGE (u:MOVIELENSUSER {userId: row.userId}) WITH u, row
MATCH (m:MOVIE {imdbID: row.movieId})
CREATE (u)-[:RATED {score: row.rating, timestamp: row.timestamp}]->(m)""")