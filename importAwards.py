from SPARQLWrapper import SPARQLWrapper, JSON
from py2neo import Graph
import progressbar as pb
import sys

user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

g = Graph(host=host, user=user, password=pwd, max_connection_lifetime=3600)

g.run("MATCH (a:AWARD) DETACH DELETE a")
g.run("MATCH (a:AWARDINSTANCE) DETACH DELETE a")

sparql = SPARQLWrapper('https://query.wikidata.org/sparql', "utf-8", "GET", agent='MS_Movies_Agent')
sparql.setReturnFormat(JSON)

sparql.setQuery(""" SELECT ?imdbID ?award ?awardLabel ?winnerImdbID
                    WHERE 
                    {
                      ?item wdt:P31 wd:Q11424.
                      ?item wdt:P345 ?imdbID.

                      ?item p:P166 ?awardStatement.
                      ?awardStatement ps:P166 ?award.

                      OPTIONAL {
                        ?awardStatement pq:P1346 ?winner.
                        ?winner wdt:P345 ?winnerImdbID.
                      }

                      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                    }
                    """)

results = sparql.query().convert()
bar = pb.ProgressBar(max_value=len(results["results"]["bindings"]))
i = 0
for result in results["results"]["bindings"]:
    i += 1
    bar.update(i)
    if 'winnerImdbID' in result.keys():
        g.run("""MATCH (m:MOVIE {imdbID: $imdbID})
                 MATCH (p:PERSON {imdbID: $winnerImdbID})
                 MERGE (a:AWARD {wikiID: $wikiID, primaryName: $awardName})
                 CREATE (ai:AWARDINSTANCE)-[:IS_A]->(a)
                 MERGE (p)<-[:AWARDED_TO]-(ai)-[:AWARDED_FOR]->(m)""",
              {'imdbID': result["imdbID"]["value"], 'winnerImdbID': result["winnerImdbID"]["value"],
               'wikiID': result["award"]["value"], 'awardName': result["awardLabel"]["value"]})
    else:
        g.run("""MATCH (m:MOVIE {imdbID: $imdbID})
                 MERGE (a:AWARD {wikiID: $wikiID, primaryName: $awardName})
                 CREATE (ai:AWARDINSTANCE)-[:IS_A]->(a)
                 MERGE (ai)-[:AWARDED_FOR]->(m)""",
              {'imdbID': result["imdbID"]["value"], 'wikiID': result["award"]["value"],
               'awardName': result["awardLabel"]["value"]})
sys.stderr.flush()