from sparqlQueries import busqueda,busquedaNome
from pprint import pprint
from anytree import Node, RenderTree

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
    

print("¿Cómo se llama?")
nome = input()
explorar(nome)
#busqueda('http://aims.fao.org/aos/agrovoc/c_6145')
#busquedaNome('water')