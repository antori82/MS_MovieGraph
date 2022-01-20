from py2neo import Graph
import progressbar as pb

g = Graph(host="143.225.233.156", user="neo4j", password="IAmJason")

g.run("MATCH (:UTTERANCE)-[r:REFERS_TO]->() DELETE r")

results= g.run("MATCH (u:UTTERANCE) WITH u, u.text_ph AS textPh, apoc.text.regexGroups(u.text_ph, \"([\\\\w\\\\s,\\\\.]*?)(\\\\[.*?\\\\])(?=([\\\\w\\\\s,\\\\.]*))\") AS list WHERE size(list) > 0 "
      "UNWIND list AS precList "
      "WITH textPh, u, precList[1] AS prec, precList[2] AS target, precList[3] AS post "
      "WITH u, textPh, u.text AS text, target, apoc.text.regexGroups(u.text, prec + \"(.*)\" + post) AS listItem, prec + \"(.*)\" + post AS regex "
      "RETURN DISTINCT ID(u) as id, textPh, regex, text, listItem[0][1] AS item, "
      "CASE"
      " WHEN target =~ '.*MOVIE_TITLE.*' THEN 'MOVIE' "
      "WHEN target =~ '.*MOVIE_GENRE.*' THEN 'GENRE' "
      "WHEN target =~ '.*MOVIE_P_ACTOR.*' THEN 'PERSON' "
      "ELSE 'None' END AS tag").data()

bar = pb.ProgressBar(max_value=len(results))
counter= 0

for result in results:
    counter += 1
    bar.update(counter)
    if result['tag'] == 'MOVIE' and result['item']:
        target= result['item'].replace('(', '\\(').replace(')', '\\)').replace('"', '\\"').replace('?', '\\?')
        query= "MATCH (u), (m:MOVIE) WHERE ID(u) = " + str(result['id']) + " AND (m.primaryTitle =~ \"(?i)" + target + "\" OR m.WikiNames =~ \"(?i)\\|\" + \"" + target + "\" + \"\\|\") CREATE (u)-[:REFERS_TO]->(m)"
        g.run(query)
    elif result['tag'] == 'PERSON' and result['item']:
        target = result['item'].replace('(', '\\(').replace(')', '\\)').replace('"', '\\"').replace('?', '\\?')
        query = "MATCH (u), (p:PERSON) WHERE ID(u) = " + str(result['id']) + " AND p.primaryName =~ \"(?i)" + target + "\" CREATE (u)-[:REFERS_TO]->(p)"
        g.run(query)