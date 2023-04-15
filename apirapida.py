from neo4j import GraphDatabase
import json
from fastapi import FastAPI 
from fastapi.responses import JSONResponse


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
    
