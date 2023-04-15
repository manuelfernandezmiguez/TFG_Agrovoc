from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

def busqueda(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?hierarchicalType ?otherConcept ?label
        WHERE { 
            BIND(<'''+parametro+'''> AS ?concept) 
            {
            ?concept skos:broader ?otherConcept . 
            BIND("broader" AS ?hierarchicalType ) 
            } UNION { 
            ?otherConcept skos:broader ?concept . 
            BIND("narrower" AS ?hierarchicalType ) 
            }
            OPTIONAL{ ?otherConcept skosxl:prefLabel/skosxl:literalForm ?label. }
            FILTER(langMatches(lang(?label), 'en')) 
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    fillos: list[str]= []
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        xerarquia = result['hierarchicalType']['value']
        value = result['label']['value']
        uri = result['otherConcept']['value']
        lista=[]
        if xerarquia!='broader':
            lista.append(value)
            lista.append(uri)
            fillos.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return fillos

def busquedaNome(nome):
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query = '''
    PREFIX skos-xl: <http://www.w3.org/2008/05/skos-xl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?concept ?conceptLabel ?broaderConcept ?broaderConceptLabel WHERE {

    # set the search term
    VALUES ?conceptLabel {"'''+nome+'''"@en}

    # get the concept matching the term
    ?concept skos-xl:prefLabel ?conceptLabelNode .
    ?conceptLabelNode skos-xl:literalForm ?conceptLabel .

    # get the broader concepts
    ?concept skos:broader ?broaderConcept.

    # and their labels
    ?broaderConcept skos-xl:prefLabel ?broaderConceptLabelNode .
    ?broaderConceptLabelNode skos-xl:literalForm ?broaderConceptLabel .

    # in English language only
    FILTER(LANGMATCHES(LANG(?broaderConceptLabel), 'en'))
    } 
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    #pprint(qres)
    for result in qres['results']['bindings']:
        uri = result['concept']['value']
        value = result['conceptLabel']['value']
        #print(f'\tValue: {value}         \tEnlace: {uri}')
        return value,uri

#busqueda('http://aims.fao.org/aos/agrovoc/c_6145')
#busquedaNome('poultry')
def busquedaNomeAlternativo(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?altlabel
        WHERE { 
          BIND(<http://aims.fao.org/aos/agrovoc/c_49904> AS ?concept) 
          OPTIONAL{ ?concept skosxl:altLabel/skosxl:literalForm ?altlabel. }
          FILTER(langMatches(lang(?altlabel), 'en')) 
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        value = result['altlabel']['value']
        lista.append(value)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return lista

def busquedaExhaustiva(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?hierarchicalType ?otherConcept ?label
        WHERE { 
            BIND(<'''+parametro+'''> AS ?concept) 
            ?otherConcept skos:broader+ ?concept . 
            BIND("narrower" AS ?hierarchicalType ) 
            OPTIONAL{ ?otherConcept skosxl:prefLabel/skosxl:literalForm ?label. }
            FILTER(langMatches(lang(?label), 'en')) 
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    fillos: list[str]= []
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        xerarquia = result['hierarchicalType']['value']
        value = result['label']['value']
        uri = result['otherConcept']['value']
        lista=[]
        if xerarquia!='broader':
            lista.append(value)
            lista.append(uri)
            fillos.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return fillos

def busquedaRelacionados(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?hierarchicalType ?otherConcept ?label
        WHERE { 
            BIND(<'''+parametro+'''> AS ?concept) 
            ?otherConcept skos:related ?concept . 
            BIND("related" AS ?hierarchicalType ) 
            OPTIONAL{ ?otherConcept skosxl:prefLabel/skosxl:literalForm ?label. }
            FILTER(langMatches(lang(?label), 'en')) 
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    relacionados: list[str]= []
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        xerarquia = result['hierarchicalType']['value']
        value = result['label']['value']
        uri = result['otherConcept']['value']
        lista=[]
        if xerarquia!='broader':
            lista.append(value)
            lista.append(uri)
            relacionados.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return relacionados

def busquedaPai(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?hierarchicalType ?otherConcept ?label
        WHERE { 
            BIND(<'''+parametro+'''> AS ?concept) 
            ?concept skos:broader ?otherConcept . 
            BIND("broader" AS ?hierarchicalType ) 
            OPTIONAL{ ?otherConcept skosxl:prefLabel/skosxl:literalForm ?label. }
            FILTER(langMatches(lang(?label), 'en'))
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    #pprint(qres)
    relacionados: list[str]= []
    for result in qres['results']['bindings']:
        value = result['label']['value']
        uri = result['otherConcept']['value']
        return value,uri
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return value,uri

def busquedaTodosPais(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?hierarchicalType ?otherConcept ?label
        WHERE { 
            BIND(<'''+parametro+'''> AS ?concept) 
            ?concept skos:broader ?otherConcept . 
            BIND("broader" AS ?hierarchicalType ) 
            OPTIONAL{ ?otherConcept skosxl:prefLabel/skosxl:literalForm ?label. }
            FILTER(langMatches(lang(?label), 'en'))
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    #pprint(qres)
    pais: list[str]= []
    lista: list[str]= []
    for result in qres['results']['bindings']:
        lista=[]
        value = result['label']['value']
        uri = result['otherConcept']['value']
        lista.append(value)
        lista.append(uri)
        pais.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return pais

def busquedaPaiExhaustiva(parametro): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT DISTINCT ?hierarchicalType ?otherConcept ?label
        WHERE { 
            BIND(<'''+parametro+'''> AS ?concept) 
            ?concept skos:broader+  ?otherConcept. 
            BIND("narrower" AS ?hierarchicalType ) 
            OPTIONAL{ ?otherConcept skosxl:prefLabel/skosxl:literalForm ?label. }
            FILTER(langMatches(lang(?label), 'en')) 
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    pais: list[str]= []
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        xerarquia = result['hierarchicalType']['value']
        value = result['label']['value']
        uri = result['otherConcept']['value']
        lista=[]
        if xerarquia!='broader':
            lista.append(value)
            lista.append(uri)
            pais.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
        
    return pais

def busquedaOrfos(): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
        SELECT ?uri ?prefLabel
        WHERE { 
            ?uri a skos:Concept .
            FILTER NOT EXISTS {?uri skos:broader ?parent}
            OPTIONAL {?uri skosxl:prefLabel/skosxl:literalForm ?prefLabel}
            FILTER(lang(?prefLabel) = 'en') 
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    fillos: list[str]= []
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        value = result['prefLabel']['value']
        uri = result['uri']['value']
        lista=[]
        lista.append(value)
        lista.append(uri)
        fillos.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
    #pprint(fillos)
    return fillos

#É equivalente a anterior consulta pero simplemente servíndose doutra das propiedades
def busquedaTopConcepts(): 
    sparql = SPARQLWrapper('https://agrovoc.fao.org/sparql')
    query='''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?uri ?prefLabel
        WHERE {
          ?uri skos:topConceptOf <http://aims.fao.org/aos/agrovoc> .
          ?uri skos:prefLabel ?prefLabel .
          FILTER (LANG(?prefLabel) = 'en')
        }
    '''
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    fillos: list[str]= []
    lista: list[str]= []
    #pprint(qres)
    for result in qres['results']['bindings']:
        value = result['prefLabel']['value']
        uri = result['uri']['value']
        lista=[]
        lista.append(value)
        lista.append(uri)
        fillos.append(lista)
            
        #print(f'Tipo: {xerarquia}\tValue: {value}         \tEnlace: {uri}')
    #pprint(fillos)
    return fillos

#nome,uri =busquedaPai("http://aims.fao.org/aos/agrovoc/c_1540")
#print(nome)
#print(uri)

#pprint(busquedaTopConcepts())


#lista = busquedaTodosPais("http://aims.fao.org/aos/agrovoc/c_1540")
#pprint(lista)

#lista = busquedaExhaustiva("http://aims.fao.org/aos/agrovoc/c_6145")
#print(lista)
#fillos=busquedaOrfos()

#lista = busquedaPaiExhaustiva("http://aims.fao.org/aos/agrovoc/c_3324")
#print(lista)
#print(busquedaNomeAlternativo('http://aims.fao.org/aos/agrovoc/c_49904'))