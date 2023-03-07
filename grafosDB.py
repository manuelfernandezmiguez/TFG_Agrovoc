from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "contrasenha"

# Connect to the Neo4j database
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define the query to retrieve nodes
query = "MATCH (n) RETURN n"

# Run the query and print the results
with driver.session() as session:
    results = session.run(query)
    for record in results:
        print(record)
        
# Close the database connection
driver.close()