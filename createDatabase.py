#This script imports IMDB data in Neo4j. Data processed with tsvProcess.py should be put in the "import" folder of your Neo4j installation
from py2neo import Graph

user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

g = Graph(host=host, user=user, password=pwd)

print("Clearing database")

g.run("""CALL apoc.periodic.commit(
          'MATCH (n) WITH n LIMIT $limit DELETE n RETURN count(*)',
          {limit: 10000}
        )
        YIELD updates, executions, runtime, batches
        RETURN updates, executions, runtime, batches""")

print("Importing titles")
g.run("""USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS from 'file:///TitleBasics_proc.tsv' as row FIELDTERMINATOR '\t' WITH row
CREATE (n:MOVIE {primaryTitle: row.primaryTitle, runtimeMinutes: toInteger(row.runtimeMinutes), imdbID: row.tconst, startYear: row.startYear, endYear: row.endYear, isAdult: row.isAdult, genres: row.genres, titleType: row.TitleType})""")

print("Importing names")
g.run("""USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS from 'file:///NamesBasics_proc.tsv' as row FIELDTERMINATOR '\t' WITH row
CREATE (n:PERSON {imdbID: row.nconst, primaryName: row.primaryName, birthYear: row.birthYear, deathYear: row.deathYear})""")

g.run("MATCH (p1:PERSON), (p2:PERSON) WHERE p1.imdbID = p2.imdbID AND p1 <> p2 CALL apoc.refactor.mergeNodes([p1,p2]) YIELD node RETURN node")

g.run("""CREATE CONSTRAINT ON (n:PERSON) ASSERT n.imdbID IS UNIQUE""")
g.run("""CREATE CONSTRAINT ON (n:MOVIE) ASSERT n.imdbID IS UNIQUE""")

print("Importing Knownfor")
g.run("""USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS from 'file:///NamesBasics_proc.tsv' as row FIELDTERMINATOR '\t' WITH row
UNWIND split(row.knownForTitles, ',') AS titles
MATCH (p:PERSON {imdbID: row.nconst})
MATCH (m:MOVIE {imdbID: titles})
MERGE (p)-[:KNOWN_FOR]->(m)""")

print("Importing principals")
g.run("""USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS from 'file:///Principals_proc.tsv' as row FIELDTERMINATOR '\t' WITH row
MATCH (m:MOVIE {imdbID: row.tconst})
MATCH (p:PERSON {imdbID: row.nconst})
MERGE (m)<-[:WORKED_IN {category: row.category, job: row.job, characters: row.characters}]-(p)""")

print("Importing episodes")
g.run("""USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS from 'file:///Episodes.tsv' as row FIELDTERMINATOR '\t' WITH row
MATCH (m:MOVIE {imdbID: row.tconst})
MATCH (p:MOVIE {imdbID: row.parentTconst})
MERGE (m)-[:EPISODE_OF {season: row.seasonNumber, episode: row.episodeNumber}]->(p)""")

print("Importing crews")
g.run("""USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS from 'file:///Crews_proc.tsv' as row FIELDTERMINATOR '\t' WITH row
MATCH (m:MOVIE {imdbID: row.tconst})
UNWIND split(row.writers, ',') AS writers
MATCH (p:PERSON {imdbID: writers})
MERGE (p)-[:WROTE]->(m) WITH m, row
UNWIND split(row.directors, ',') AS directors
MATCH (p:PERSON {imdbID: directors})
MERGE (p)-[:DIRECTED]->(m)""")

print("Setting properties")
genres= g.run("MATCH (n:MOVIE) UNWIND SPLIT(n.genres, \",\") AS genres WITH genres RETURN DISTINCT genres")

for genre in genres:
    print(genre[0])
    if genre[0] != '\\N':
        g.run("MATCH (n:MOVIE) WHERE n.genres CONTAINS '" + genre[0] + "' SET n:" + genre[0].upper().replace("-", "_"))

g.run("MATCH(n:MOVIE) REMOVE n.genres, n.isAdult")

for property in ['primaryTitle', 'runtimeMinutes', 'startYear', 'endYear', 'titleType']:
    g.run("call apoc.periodic.iterate(\"MATCH (n:MOVIE) WHERE n." + property + " = '\\\\N' RETURN n\", \"REMOVE n." + property + "\", {batchSize:1000}) yield batches, total return batches, total")

for property in ['primaryName', 'birthYear', 'deathYear']:
    g.run("call apoc.periodic.iterate(\"MATCH (n:PERSON) WHERE n." + property + " = '\\\\N' RETURN n\", \"REMOVE n." + property + "\", {batchSize:1000}) yield batches, total return batches, total")



