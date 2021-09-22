import progressbar as pb
from py2neo import Graph
from SPARQLWrapper import SPARQLWrapper, JSON

user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

g = Graph(host=host, user=user, password=pwd)

sparql = SPARQLWrapper('https://query.wikidata.org/sparql', "utf-8", "GET", agent='MS_Movies_Agent')
sparql.setReturnFormat(JSON)

imdbIDs = [d['imdbID'] for d in g.run(
    "MATCH (m:MOVIE)<-[:RATED]-(:MOVIELENSUSER) WHERE NOT EXISTS(m.WikiNames) RETURN DISTINCT m.imdbID AS imdbID").data()]

bar = pb.ProgressBar(max_value=len(imdbIDs))
counter = 0

for item in imdbIDs:
    counter += 1
    bar.update(counter)
    sparql.setQuery("""SELECT ?item ?itemLabel (group_concat(?altEN;separator="|") as ?altENs)
    WHERE 
    {
      ?item wdt:P31 wd:Q11424.
      ?item wdt:P345 '""" + item + """'.

      OPTIONAL{
        ?item skos:altLabel ?altEN
        FILTER (lang(?altEN) = "en")
      }

      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    GROUP BY ?item ?itemLabel ?altENs""")

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        names = "|" + result['itemLabel']['value'] + "|" + result['altENs']['value'] + "|" if result['altENs'][
                                                                                                  'value'] != "" else "|" + \
                                                                                                                      result[
                                                                                                                          'itemLabel'][
                                                                                                                          'value'] + "|"
        g.run("MATCH (m:MOVIE {imdbID: '" + item + "'}) SET m.WikiNames= \"" + names.replace("\"", "\\\"") + "\"")
        pass