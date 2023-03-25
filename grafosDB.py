from neo4j import GraphDatabase
import json

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "contrasenha"

# Connect to the Neo4j database
driver = GraphDatabase.driver(uri, auth=(username, password))


def crearNodo(nome,uri):
    nome = nome.replace("'", "")
    query = "CREATE (skos:Concept {label:"+ f"'{nome}'"+", uri: "+f"'{uri}',"+ "graph: 'AGROVOC'})"
    with driver.session() as session:
        session.run(query)

def crearRelacion(nome,nome2,tipoRelacion):
    nome = nome.replace("'", "")
    nome2 = nome2.replace("'", "")
    query = f"""
    MATCH
    (a:Concept),
    (b:Concept)
    WHERE a.label = '{nome}' AND b.label = '{nome2}'
    CREATE (a)-[r:{tipoRelacion}]->(b)
    RETURN type(r)

    """

    with driver.session() as session:
        session.run(query)
        

def comprobarExistencia(nome):
    nome = nome.replace("'", "")
    query = "OPTIONAL MATCH (n:Concept {label: "+f"'{nome}'"+"}) RETURN n.label AS label"
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:

            if node["label"] is None:
                return False
            else:
                return True
            
def comprobarExistenciaRelacion(nome,nome2,nomeRelación):
    nome = nome.replace("'", "")
    nome2 = nome2.replace("'", "")
    query="MATCH  (p:Concept {label:"+f"'{nome}'"+"}), (b:Concept {label:"+f"'{nome2}'"+"}),( (b)-[:"+f"{nomeRelación}"+"]-(p) )  RETURN b.label AS label"
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:
            if node["label"] is None:
                return False
            else:
                return True


#query = "MATCH (n:Concept) WHERE n.label='chiken' RETURN properties(n)"
# Run the query and print the results


        
# Close the database connection

###
def get_some_data(limit) :
    lista: list[json_data]= []
    query = "MATCH (n:Concept) WHERE n.label='chiken' RETURN properties(n) LIMIT " + str(limit)
    query = "MATCH (n) RETURN n{label: n.label, graph:n.graph} "
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data:json = json.dumps(record)
            lista.append(json_data)
        
        return lista
###
#json_data = json.dumps(get_some_data(limit=1).data())
#print(json_data)
#print(get_some_data(limit=5))

driver.close()