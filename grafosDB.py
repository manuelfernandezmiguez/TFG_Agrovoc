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

def crearRelacion(uri,uri2,tipoRelacion):
    uri = uri.replace("'", "")
    uri2 = uri2.replace("'", "")
    query = f"""
    MATCH
    (a:Concept),
    (b:Concept)
    WHERE a.uri = '{uri}' AND b.uri = '{uri2}'
    CREATE (a)-[r:{tipoRelacion}]->(b)
    RETURN type(r)

    """

    with driver.session() as session:
        session.run(query)

def fixarAlcume(nome,nomes):
    nome = nome.replace("'", "")
    query = f"""
    MATCH (c:Concept)
    WHERE c.label = '{nome}'
    SET c.alternative_labels = '{', '.join(nomes).replace("'", "")}'

    """

    with driver.session() as session:
        session.run(query)   

def fixarAlcumeLexSte(nome,lex,stem):
    lista=[]
    for a in stem:
        lista+=a
    lista2=[]
    for l in lex:
        lista2+=l
    #print(lista)
    #print((lex))
    nome = nome.replace("'", "")
    query = f"""
    MATCH (c:Concept)
    WHERE c.label = '{nome}'
    SET c.alternative_labels_stem = '{', '.join(lista).replace("'", "")}'
    SET c.alternative_labels_lex = '{', '.join(lista2).replace("'", "")}'
    """

    with driver.session() as session:
        session.run(query)
def fixarNomeLexSte(nome,lex,stem):
    nome = nome.replace("'", "")
    if len(nome.split())>1:
        query = f"""
        MATCH (c:Concept)
        WHERE c.label = '{nome}'
        SET c.label_stem = '{', '.join(stem).replace("'", "")}'
        SET c.label_lex = '{', '.join(lex).replace("'", "")}'

        """
    else:
        query = f"""
        MATCH (c:Concept)
        WHERE c.label = '{nome}'
        SET c.label_stem = '{stem[0].replace("'", "")}'
        SET c.label_lex = '{lex[0].replace("'", "")}'

        """

    with driver.session() as session:
        session.run(query)     

def crearArtigo(titulo,resumo,uri):
    uri = uri.replace("'", "")
    titulo = titulo.replace("'", "")
    resumo = resumo.replace("'", "")

    query = "CREATE (a:Artigo {titulo:"+ f"'{titulo}'"+", resumo: "+f"'{resumo}',"+ "uri: "+f"'{uri}'"+ "})"
    with driver.session() as session:
        session.run(query)
def devolverArtigo(uri:str):
    uri = uri.replace("'", "")
    query = f"""MATCH(a:Artigo) where a.uri='{uri}' Return a"""
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:
            return node
#print(devolverArtigo("https://www.sciencedirect.com/science/article/pii/S0168169916000168"))
def crearClasificación(uri,uri2):
    uri = uri.replace("'", "")
    uri2 = uri2.replace("'", "")
    query = f"""
    MATCH
    (a:Artigo),
    (b:Concept)
    WHERE a.uri = '{uri}' AND b.uri = '{uri2}'
    CREATE (a)-[r:Ten_anotado]->(b)
    RETURN type(r)

    """

    with driver.session() as session:
        session.run(query)

def obter_conceitos_neo4j(string):
    string = string.replace("'", "")
    # Consulta para obter os conceitos presentes na string
    query = f"""
    WITH '{string}' AS input
    WITH split(input, ' ') AS elements
    UNWIND elements AS element
    MATCH (c:Concept)
    WHERE c.label CONTAINS  element OR c.alternative_labels CONTAINS element
    RETURN element, collect(c.label) AS matchingLabels
    """

    with driver.session() as session:
        result = session.run(query, string=string)
        elements = []
        matching_labels = []
        for record in result:
            elements.append(record['element'])
            matching_labels.append(record['matchingLabels'])

    # Imprima as listas
    #print("Elements:", elements)
    #print("Matching Labels:", matching_labels)
    # Fechar a conexão com o Neo4j
    driver.close()

    return elements,matching_labels

def comprobarExistencia(uri):
    uri = uri.replace("'", "")
    query = "OPTIONAL MATCH (n:Concept {uri: "+f"'{uri}'"+"}) RETURN n.uri AS uri"
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:

            if node["uri"] is None:
                return False
            else:
                return True
def devolverContaFillos(nome:str):
    query = f"""
    MATCH p=(q)-[r:Narrower]->() where q.label='{nome}' or q.alternative_labels contains '{nome}' RETURN COUNT(p) as conta
    """
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:
            return node['conta']
        
#print(devolverContaFillos('oil and gas production'))
def comprobarExistenciaNome(nome):
    nome = nome.replace("'", "")
    query="OPTIONAL MATCH (n) WHERE n.label = "+f"'{nome}'"+" OR "+f"'{nome}'"+" IN n.alternative_labels RETURN n as node"
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:

            if node["node"] is None:
                return False
            else:
                return True

def devolverNodoPoloNome(nome):
    lista: list[json_data]= []
    listaAuxiliar=['aux','aux','aux']
    nome = nome.replace("'", "")
    query="MATCH (n) WHERE n.label = "+f"'{nome}'"+" OR n.alternative_labels CONTAINS "+f"'{nome}'"+"   RETURN n.label,n.alternative_labels,n.uri"
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        if(len(lista)>3):
            listaAuxiliar[0]=lista[0]
            listaAuxiliar[1]=lista[1]
            listaAuxiliar[2]=lista[2]
            lista=listaAuxiliar
        return lista
#print(comprobarExistencia('http://aims.fao.org/aos/agrovoc/c_3654'))
#print(devolverNodoPoloNome('computer system'))
#print(comprobarExistenciaNome('poultry'))
            
def comprobarExistenciaRelacion(uri,uri2,nomeRelación):
    uri = uri.replace("'", "")
    uri2 = uri2.replace("'", "")
    query = "MATCH p=(n:Concept)-[r:"+nomeRelación+"]->(n2:Concept) WHERE n.uri="+f"'{uri}'"+" AND n2.uri="+f"'{uri2}'"+" RETURN r"
    #query="MATCH  (p:Concept {label:"+f"'{nome}'"+"}), (b:Concept {label:"+f"'{nome2}'"+"}),( (b)-[:"+f"{nomeRelación}"+"]->(p) )  RETURN b.label AS label"
    with driver.session() as session:
        nodes =  session.run(query)
        for node in nodes:
            if node is None:
                return False
            else:
                return True
            
def devolverLex(nome:str):
    query = f"""
    MATCH(e) where e.label='{nome}' e.alternative_labels='{nome}' return e.label_stem
    """
    lista=[]
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
    return lista

def buscarLexContidoConcepto(nome1:str,nome2:str):
    lista: list[json_data]= []
    query = f"""
    MATCH (e)-[:Narrower*]->(b)
    WHERE e.label = '{nome1}' AND b.alternative_labels CONTAINS '{nome2}' 
    RETURN distinct b.label
    """

    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
        return lista
def StringContenLexConcepto(text:str):
    lista: list[json_data]= []
    listaResultado: list[json_data]= []
    text = text.replace("'", "")
    query = f"""
    MATCH (n:Concept)
    Where  n.alternative_labels = "{text}" or '{text}' = n.label or n.alternative_labels contains "{text}" or '{text}' contains n.label or n.label contains '{text}' or '{text}' contains n.alternative_labels
    RETURN n.label,n.alternative_labels,n.uri
    """

    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
            listaResultado.append(lista)
            lista=[]
        return listaResultado
#print(StringContenLexConcepto('computer vision'))
#print(buscarLexContidoConcepto('housing','bee'))
def contidosNosFillos(nome:str):
    query = f"""
    MATCH (me)-[:Narrower*]->(remote_friend),(p)-[:Contido_en*]->(remote_friend)
    WHERE me.label = '{nome}'
    RETURN remote_friend.label,p.label
    """
    with driver.session() as session:
        result = session.run(query=query)
        nodes = result.data()
    return nodes

def contidoNosConceptosSimilares(nome:str,nome2:str):
    lista: list[json_data]= []
    listaResultado: list[json_data]= []
    query = f"""
    MATCH (q)-[:Broader]->(r),(r)-[:Narrower]->(p),(s)-[:Contido_en]->(p)
    Where  q.label='{nome2}' and s.label='{nome}'
    RETURN p.label,p.alternative_labels,p.uri
    """
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
            listaResultado.append(lista)
            lista=[]
        return listaResultado
#print(contidoNosConceptosSimilares("light","sensors"))
def paisContidosNosFillos(nome1:str,nome2:str):
    lista: list[json_data]= []
    query = f"""
    MATCH (e)-[:Narrower*]->(b),(c)-[:Contido_en]->(b),(d)-[:Broader*]->(c)
    WHERE d.label='{nome1}' AND e.label='{nome2}'
    RETURN distinct b.label
    """

    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
        return lista
def buscarTermoContidoConcepto(nome1:str,nome2:str):
    lista: list[json_data]= []
    query = f"""
    MATCH (e)-[:Narrower*]->(b),(d)-[:Contido_en]->(c),(d)-[:Contido_en]->(b)
    WHERE c.label='{nome1}' AND e.label='{nome2}'
    RETURN distinct b.label
    """

    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
        return lista
#print(buscarTermoContidoConcepto('oil crops','production'))
def buscarConceptoContido(nome1:str,nome2:str):
    lista: list[json_data]= []
    query = f"""
    MATCH (e)-[:Narrower*]->(b),(c)-[:Contido_en]->(b)
    WHERE c.label='{nome1}' AND e.label='{nome2}'
    RETURN distinct b.label
    """

    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
        return lista
#print(buscarTermoContidoConcepto("honey bees","production"))
#query = "MATCH (n:Concept) WHERE n.label='chiken' RETURN properties(n)"
# Run the query and print the results



# Close the database connection

###
def get_some_data(limit) :
    lista: list[json_data]= []
    query = "MATCH (n:Concept) WHERE n.label='chiken' RETURN properties(n) LIMIT " + str(limit)
    query = "MATCH (n) WHERE n.label='poultry' RETURN n{label: n.label, graph: n.graph} "
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data:json = json.dumps(record)
            lista.append(json_data)
        
        return lista
    
def busquedaTermosConcepto(concepto1,concepto2) :
    lista: list[json_data]= []
    query = f"MATCH (n) WHERE n.label='{concepto1}' OR n.label='{concepto2}' RETURN n.label as label  "
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
        return lista
    
def busquedaPaisGrafo(concepto1) :
    lista: list[json_data]= []
    query = "MATCH (n:Concept)-[:Broader*]->(p:Concept) where n.label="+f"'{concepto1}'"+" or n.alternative_labels="+f"'{concepto1}'"+"RETURN p.label as label "
    with driver.session() as session:
        results =  session.run(query)
        for record in results:
            json_data = record
            lista+=(json_data)
        
        return lista

#print(busquedaPaisGrafo('honeybees'))
###
#json_data = json.dumps(get_some_data(limit=1).data())
#print(json_data)
#print(busquedaTermosConcepto("animals","poultry"))
#print(busquedaPaisGrafo("chemistry"))
#proba = comprobarExistenciaRelacion("http://aims.fao.org/aos/agrovoc/c_c3ea7f1d","http://aims.fao.org/aos/agrovoc/c_28279","Broader*")
#if proba:
    #print('a')
#proba = comprobarExistencia("useful animals")
#print(proba)
driver.close()