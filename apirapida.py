from neo4j import GraphDatabase
import json
from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from xeneral import facerBusquedaDoConcepto,ConceptosAgrovocNoTexto,TratarTextoCientifico
from grafosDB import contidosNosFillos
app = FastAPI()
uri = "neo4j://localhost:7687"
username = "neo4j"
password = "contrasenha"

# Connect to the Neo4j database
driver = GraphDatabase.driver(uri, auth=(username, password))

@app.get("/")
def default():
    return{"response":"you are in the root"}
@app.get("/neo4j/nodes/all")
async def list_all_nodes():
    query = f"""
        MATCH (node)
        RETURN node"""
    try:
        with driver.session() as session:
            result = session.run(query=query)
            nodes = result.data()
        return nodes
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "listing all nodes unsuccessful"}, status_code=500)

@app.get("/neo4j/node/id/{id}")
async def get_node_id(id:int):
    query = f"""
        MATCH (node:Concept)
        WHERE ID(node) = {id}
        RETURN node"""
    try:
        with driver.session() as session:
            result = session.run(query=query)
            nodes = result.data()
        return nodes
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)
    
@app.get("/neo4j/node/nome/{nome}")
async def get_node_nome(nome:str):
    query = f"""
        MATCH (node:Concept)
        WHERE node.label = '{nome}'
        RETURN node"""
    try:
        with driver.session() as session:
            result = session.run(query=query)
            nodes = result.data()
        return nodes
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)
    
@app.get("/neo4j/contidos/nome/{nome}/nome/{nome2}")
async def get_node_nome(nome:str,nome2:str):
    query = f"""
    MATCH (e)-[:Narrower*]->(b),(b)-[:Contido_en]->(c),(c)-[:Broader*]->(d)
    WHERE d.label='{nome}' AND e.label='{nome2}'
    RETURN distinct b.label
    """
    try:
        with driver.session() as session:
            result = session.run(query=query)
            nodes = result.data()
        return nodes
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)
    

@app.get("/neo4j/contidos/nome/{nome}")
async def get_node_nome(nome:str):
    query = f"""
    MATCH (me)-[:Narrower*]->(remote_friend),(p)-[:Contido_en*]->(remote_friend)
    WHERE me.label = '{nome}'
    RETURN remote_friend.label,p.label
    """
    try:
        with driver.session() as session:
            result = session.run(query=query)
            nodes = result.data()
        return nodes
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)
    

@app.get("/neo4j/busqueda/nome/{nome}")
async def get_busqueda_nome(nome:str):
    lista=facerBusquedaDoConcepto(nome)
    
    try:
        return lista
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)
    
@app.get("/neo4j/lexical/stem/{stem}")
async def get_nodes_by_stem(stem:str):
    query = f"""
    MATCH (me)-[:Narrower*]->(remote_friend),(p)-[:Contido_en*]->(remote_friend)
    WHERE me.label = '{stem}'
    RETURN remote_friend.label,p.label
    """
    try:
        with driver.session() as session:
            result = session.run(query=query)
            nodes = result.data()
        return nodes
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)

@app.get("/neo4j/lexical/busqueda/{string}")
async def get_node_by_string_search(string:str):
    resultado = facerBusquedaDoConcepto(string)
    try:
        return resultado
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)

@app.post("/neo4j/anotacion/{titulo}")
async def get_node_by_string_search(titulo:str,string:str,uri:str):
    resultado = TratarTextoCientifico(titulo,string,uri)
    try:
        return resultado
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "get location node unsuccessful"}, status_code=500)