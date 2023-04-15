from sparqlQueries import busqueda,busquedaNome,busquedaExhaustiva,busquedaPai,busquedaOrfos,busquedaPaiExhaustiva,busquedaRelacionados,busquedaNomeAlternativo,busquedaTodosPais
from nltkFuncions import dividirTexto,aplicarStemming,aplicarStemmingIndividual,aplicarPlural,estaEnIngles
from parseCSV import escribir
from pprint import pprint
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from grafosDB import crearNodo,crearRelacion,comprobarExistencia,comprobarExistenciaRelacion
import os

d = {}
def procesar_relacionados(nome:str,uri:str):
    relacionados =busquedaRelacionados(uri)
    for result in relacionados:
        if(comprobarExistencia(result[0])==False):
            crearNodo(result[0],result[1])
        if(comprobarExistenciaRelacion(nome,result[0],"Relacionado")==None):
            crearRelacion(nome,result[0],"Relacionado")
        

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
#esta función
#a variable latin serve para diferenciar as chamadas dende o resto dos TOP concepts de organismos, que debido a ter termos en latin ten que filtralos
def ConceptosPalabras(texto: str,latin:bool):
    ingles:bool = False
    listaNomes: list[str]= []
    nome,uri = busquedaNome(texto)
    if(comprobarExistencia(nome)==False):
        crearNodo(nome,uri)
    
    
    fillos = busquedaExhaustiva(uri)
    print(f"este é o número de conceptos da mostra que imos analizar:  {len(fillos)} descendentes do seguinte concepto pai {nome}")
    for i,f in enumerate(fillos):
        print("analizamos o seguinte concepto: "+f[0])
        if latin == True:
            ingles = False #serve para logo ver se facemos as relacions contido_en no caso de que sexa un termo que conten moitos conceptos en latin
            if(estaEnIngles(f[0])):
                ingles=True
            else:
                for alternativo in busquedaNomeAlternativo(f[1]):
                    if(estaEnIngles(alternativo)):
                        f[0]=alternativo
                        ingles=True
        analizar=dividirTexto(f[0].replace("'", ""))
        if(comprobarExistencia(f[0])==False):
            crearNodo(f[0],f[1])
        procesar_relacionados(f[0],f[1])
        nome,uri = busquedaNome(f[0])
        paiNome,pai=busquedaPai(uri)
        listaPais = busquedaTodosPais(uri)
        if len(listaPais)>1:
            for fi in listaPais:
                print("ENTRAMOS AQUI "+fi[0])
                if(comprobarExistencia(fi[0])==False):
                    crearNodo(fi[0],fi[1])
                if(comprobarExistenciaRelacion(f[0],fi[0],"Broader")==None):
                    crearRelacion(f[0],fi[0],"Broader")
                if(comprobarExistenciaRelacion(fi[0],f[0],"Narrower")==None):
                    crearRelacion(fi[0],f[0],"Narrower")
        
        pais=busquedaPaiExhaustiva(uri)
        #print("este e o concepto: "+f[0]+"e este é o pai: "+paiNome)
        if(comprobarExistenciaRelacion(f[0],paiNome,"Broader")==None):
            crearRelacion(f[0],paiNome,"Broader")
        if(comprobarExistenciaRelacion(paiNome,f[0],"Narrower")==None):
            crearRelacion(paiNome,f[0],"Narrower")
        tamano = len(analizar)
        if(tamano>1):
            #nome,uri = busquedaNome(f[0])
            ij=0
            for a in analizar:
                ij+=1
                if(ij<0):#se aumentamos o i artificialmente xa saimos que xa conseguimos a palabra
                    break
                if(tamano>2 and ij<(tamano)):#se hai polo menos 2 palabras antes da palabra final tentamos probar se hai un concepto de duas palabras contido
                    a=analizar[ij-1] + ' ' + aplicarPlural(analizar[ij])
                    if(busquedaNome(a) is not None):
                        #print('entra aqui?')
                        ij=-2  
                    else:
                        a=analizar[ij-1] + ' ' + (analizar[ij])
                        if(busquedaNome(a) is not None):
                            #print('entra aqui?')
                            ij=-2
                        else:
                            #print('non entra aqui e ten este nome: '+analizar[ij-1])
                            a=analizar[ij-1]
                if(busquedaNome(a) is None):
                    #print('entrou: '+a)
                    a=aplicarPlural(a)
                if(busquedaNome(a) is not None):
                    #print('entrou2: '+a)
                    nomeA,uriNome = busquedaNome(a) 
                    #paiNome,pai=busquedaPai(uri)
                    if(aplicarStemmingIndividual(nomeA) in aplicarStemming(paiNome)):
                        break
                    if(nomeA in dividirTexto(paiNome)): #se o nome do noso elemento A buscado a partir do string sacado de f[0] por medio dun tokenizer coincide co pai do elemento f[0].
                        break
                    ###este é o código para que todos os descendentes dunha palabra(housing) que a conteñan (cattle housing) non sexan contados,incluso ainda que o seu pai non a teña
                    romper=False
                    for p in pais:
                        ancestroNome=p[0]
                        if(nomeA in dividirTexto(ancestroNome)):
                            romper=True
                            break
                    if(romper==True):
                        break

                    
                    print(f"nome: {nome} busquedadoPai: {paiNome} nomeA: {nomeA} indice: {i}")
                    if(comprobarExistencia(nomeA)==False):
                        crearNodo(nomeA,uriNome)
                    procesar_relacionados(nomeA,uriNome)
                    if(latin==True and ingles==True):
                        if(comprobarExistenciaRelacion(nomeA,nome,"Contido_en")==None):
                            crearRelacion(nomeA,nome,"Contido_en")
                    elif(latin!=True):
                        if(comprobarExistenciaRelacion(nomeA,nome,"Contido_en")==None):
                            crearRelacion(nomeA,nome,"Contido_en")
                    else: 
                        break
                    auxiliar=[nome,uri,nomeA,uriNome]
                    listaNomes.append(auxiliar)  
                      
    return listaNomes



#print("¿Cómo se llama?")
#nome = input()
#explorar(nome)
def gardarConsultaAccesos(nome: str):
    listaEscribir=ConceptosPalabras(nome,False)
    gardar= "csvs/"+nome + ".csv"
    #print(listaEscribir)
    cabeceira=['nome', 'uriVella',"NovoElemento","uriNiovo"]
    escribir(gardar,listaEscribir,cabeceira)


def gardadoXeralConsultaAccesos():
    mandar:bool = False
    listaEscribir: list[str]= []
    listaParcial: list[str]= []
    listaInicial=busquedaOrfos()
    cabeceira=['nome', 'uriVella',"NovoElemento","uriNiovo"]
    
    for l in listaInicial:
        mandar=False
        if(comprobarExistencia(l[0])==False):
            crearNodo(l[0],l[1])
        procesar_relacionados(l[0],l[1])
        listaEscribir=[]
        gardar="csvs/"+l[0] + ".csv"
        print(f"\n IMOS EXPLORAR AGORA ESTE CONCEPTO INICIAL: {l[0]} \n")
        if l[0] == 'organisms': 
            mandar=True    # continue here
        if os.path.exists(gardar) :
            continue
        listaFillos=busqueda(l[1])
        
        for i in listaFillos:    
            listaParcial=[]
            print("iste é un dos fillos: "+i[0]+"dos fillos dun concepto top, que é: "+l[0])
            if(i[0] is not None):
                if(comprobarExistencia(i[0])==False):
                    crearNodo(i[0],i[1])
                if(comprobarExistenciaRelacion(i[0],l[0],"Broader")==None):    
                    crearRelacion(i[0],l[0],"Broader")
                if(comprobarExistenciaRelacion(l[0],i[0],"Narrower")==None):
                    crearRelacion(l[0],i[0],"Narrower")
                procesar_relacionados(i[0],i[1])
                listaParcial+=ConceptosPalabras(i[0],mandar)
            
            #pprint(listaParcial)
            listaEscribir+=listaParcial
            #pprint(listaEscribir)
        escribir(gardar,listaEscribir,cabeceira)
        
    gardar= "csvs/xeral.csv"
    #print(listaEscribir)
    cabeceira=['nome', 'uriVella',"NovoElemento","uriNiovo"]
    escribir(gardar,listaEscribir,cabeceira)


#busqueda('http://aims.fao.org/aos/agrovoc/c_6145')
#gardadoXeralConsultaAccesos()
#boleo = os.path.exists("csvs/feeding.csv")
#print(boleo)
#gardarConsultaAccesos("housing")
#busquedaNome('water')