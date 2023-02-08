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
