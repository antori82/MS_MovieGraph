import pandas as pd
from py2neo import Graph
import numpy as np

user= "PUT_YOUR_NEO4J_USERNAME_HERE"
pwd= "PUT_YOUR_NEO4J_PASSWORD_HERE"
host= "PUT_YOUR_NEO4J_IP_HERE"

graph = Graph(host=host, user=user, password=pwd, max_connection_lifetime=3600)

df = pd.read_csv("newtrain.tsv", delimiter='\t')

graph.run("MATCH (n:UTTERANCE) DETACH DELETE n")

lista_text =[]
for i in df['text']:
    lista_text.append(i)
current_phrase = ""
previous_phrase = ""
current_id = ""
column = df['text_with_placeholder']
dialog_id = df['dialog_id']
for i, item in enumerate(column):
    if current_id != dialog_id[i]:              
        previous_phrase = ""           
    current_id = dialog_id[i]          
    if item != "" and item != "text_with_placeholder" and type(item) is str :
        current_phrase = item                   
        label = ""
        if pd.notna(df['expert_label'][i]):
            label = ":" + df['expert_label'][i]
        if previous_phrase == "":
            prev_id = graph.run("CREATE (u:UTTERANCE:" + df['speaker'][i] + label + "{text_ph: $text_ph, text: $text, turn_id: $turn_id, dialogue_id: $dialogue_id})  return id(u) as id", parameters= {"text_ph":current_phrase, "text": df['text'][i], "turn_id": np.asscalar(df["turn_id"][i]), "dialogue_id": df["dialog_id"][i]}).data()[0]['id']
        else:
            prev_id = graph.run("MATCH (u:UTTERANCE) where id(u) = $id CREATE (u2:UTTERANCE:"+df['speaker'][i]+label+"{text_ph: $text_ph, text: $text, turn_id: $turn_id, dialogue_id: $dialogue_id}) CREATE (u)-[:FOLLOWED_BY]-> (u2) RETURN id(u2) as id", parameters= {"id": prev_id, "text_ph": current_phrase, "text": df['text'][i], "turn_id": np.asscalar(df["turn_id"][i]), "dialogue_id": df["dialog_id"][i]}).data()[0]['id']
        previous_phrase = current_phrase