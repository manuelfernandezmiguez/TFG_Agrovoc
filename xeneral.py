from sparqlQueries import busqueda,busquedaNome,busquedaExhaustiva,busquedaPai
from nltkFuncions import dividirTexto
from parseCSV import escribir
from pprint import pprint
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

d = {}

def explorar(nome: str):
    lista: list[str]= []
    nome,uri = busquedaNome(nome)
    #print(f'Nome: {nome} e a uri: {uri}')
    A = Node(nome)
    key=nome
    d[key] = A
    #print(key)
    #print(d[key])
    #fillos = busqueda(uri)
    #print(fillos)
    lista.append([nome,uri])
    i=0
    while(len(lista)!=0 ):
        
        pai=lista.pop()
        fillos = busqueda(pai[1])
        #print(pai)
        anterior_dkey=d[pai[0]]
        while(len(fillos)!=0):
            i+=1
            fillo=fillos.pop()
            lista.append(fillo)
            
            key=fillo[0]
            d[key] = Node(fillo[0], parent=anterior_dkey)
            #print(fillo[0])
    for pre, fill, node in RenderTree(A):
        print("%s%s" % (pre, node.name))
    imaxe= "imxs/"+nome+".png"
    DotExporter(A).to_picture(imaxe)

def ConceptosPalabras(texto: str):
    listaNomes: list[str]= []
    nome,uri = busquedaNome(texto)
    fillos = busquedaExhaustiva(uri)
    print(f"este é o número de conceptos da mostra que imos analizar:  {len(fillos)}")
    for i,f in enumerate(fillos):
        #print(f[0])
        analizar=dividirTexto(f[0])
        if(len(analizar)>1):
            nome,uri = busquedaNome(f[0])
            for a in analizar:
                if(busquedaNome(a) is not None):
                    nomeA,uriNome = busquedaNome(a) 
                    paiNome,pai=busquedaPai(uri)
                    print(f"nome: {nome} nomeA: {nomeA} indice: {i}")

                    if(nomeA in dividirTexto(paiNome)): #se o nome do noso elemento A buscado a partir do string sacado de f[0] por medio dun tokenizer coincide co pai do elemento f[0].
                        break
                    #print('analizar')
                    auxiliar=[nome,uri,nomeA,uriNome]
                    listaNomes.append(auxiliar)
        
    return listaNomes



#print("¿Cómo se llama?")
#nome = input()
#explorar(nome)
def gardarConsultaAccesos(nome: str):
    listaEscribir=ConceptosPalabras(nome)
    gardar= "csvs/"+nome + ".csv"
    #print(listaEscribir)
    cabeceira=['nome', 'uriVella',"NovoElemento","uriNiovo"]
    escribir(gardar,listaEscribir,cabeceira)


#busqueda('http://aims.fao.org/aos/agrovoc/c_6145')


#busquedaNome('water')