from sparqlQueries import busquedaInmediataIncludesUse,busquedaInmediata,busquedaExhaustivaIncludesUse,buscarUsedOf,buscarInluidos,busquedaWikidataIDAgrovoc,comprobarXerarquia,busqueda,busquedaNome,busquedaExhaustiva,busquedaPai,busquedaOrfos,busquedaPaiExhaustiva,busquedaRelacionados,busquedaNomeAlternativo,busquedaTodosPais
from nltkFuncions import devolverConceptosWikidata,getSingular,aplicarPluralFrase,extraerKeywords,dividirTexto,aplicarStemming,aplicarStemmingIndividual,aplicarPlural,estaEnIngles,combinacionParaBusqueda,aplicarStemmingLista,lexemaLista,lexemaConcepto,lexemaTermo
from parseCSV import escribir
from pprint import pprint
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from grafosDB import ContidoUnion,busquedaFillosGrafo,devolverLemma,devolverStemma,startsWithStem,devolverContaFillos,crearClasificación,devolverArtigo,crearArtigo,devolverNodoPoloNome,contidoNosConceptosSimilares,StringContenLexConcepto,buscarLexContidoConcepto,devolverLex,buscarTermoContidoConcepto,buscarConceptoContido,contidosNosFillos,crearNodo,crearRelacion,comprobarExistencia,comprobarExistenciaRelacion,busquedaPaisGrafo,paisContidosNosFillos,fixarAlcume,fixarAlcumeLexSte,fixarNomeLexSte,comprobarExistenciaNome
from conversaLLM import funcionchat
import time
import os

d = {}
def anotarWikidataAgrovoc(texto):

    entities = (devolverConceptosWikidata(texto))
    for entity in entities:
        print(entity)
        print(busquedaWikidataIDAgrovoc('Q'+str(entity.identifier)))
#anotarWikidataAgrovoc("The raspberry pi is a microcomputer used to AI and IOT")
def lexemaEstemma(nome:str,lista:list):
    fixarNomeLexSte(nome,lexemaConcepto(nome),aplicarStemming(nome))
    if(len(lista)>0):
        fixarAlcumeLexSte(nome,lexemaLista(lista),aplicarStemmingLista(lista))
def facerBusquedaDoConcepto(nome:str):
    lista = []
    listaPais = []
    listaResultado = []
    if(comprobarExistenciaNome(nome)==False):
        for palabra in combinacionParaBusqueda(nome):
            if(comprobarExistenciaNome(palabra)==True):
                lista.append(palabra)
    else:
        lista.append(nome)
        return lista
    #print(lista)
    if(len(lista)>2):
        #print('entra aqui')
        size=0
        guardar=None
        for l in lista:
            if len(l.split())>size and lista[-1] not in l:
                size=len(l.split())
                guardar=l
        lista=[]
        if guardar is not None:
            lista.append(guardar)
        for d in dividirTexto(nome):
            guardar=d
        if guardar is not None:
            lista.append(guardar)
    #print(lista)
    i=0

    if(len(lista)>1):
        listaPais.append(lista[0])
        listaPais+=busquedaPaisGrafo(lista[0])
        
        #print(listaPais)
    resultado=None
    contador=1000
    if(len(lista)==2):
        #print("entra aqui")
        for lp in listaPais:
            #print("concepto analizado: "+lp +"\t concepto a cotexar "+lista[1])
            resultadoParcial=[]
            resultadoParcial=buscarConceptoContido(lp,lista[1])
            #print(resultadoParcial)
            if(len(resultadoParcial)==0):
                resultadoParcial=buscarTermoContidoConcepto(lp,lista[1])
            if len(resultadoParcial)!=0:
                #listaNova=contidosNosFillos(lp)
                #pprint(listaNova)
                #print(resultadoParcial)
                contadorParcial=devolverContaFillos(lp)
                if(contadorParcial<contador):
                    contador=contadorParcial
                    resultado=resultadoParcial
    if resultado is not None:
        for i in resultado:
            if lista[-1] in i.split() :
                guardar=i
                resultado=[]
                resultado.append(i)
    print(nome)
    print(resultado)
    return resultado
def facerBusqueda2Concepto(nome1,nome2):
    resultado=[]
    resultado=ContidoUnion(nome1,nome2)[0]
    return resultado
#print(facerBusqueda2Concepto('honey bees','housing'))
#print(buscarConceptoContido('chickens','housing'))
#pprint(facerBusquedaDoConcepto('honey bees housing'))
#pprint(facerBusquedaDoConcepto('forage sorghum production'))
#print(combinacionParaBusqueda('calves housing'))
def sortFunc(e):
  return e[3]
def ConceptosAgrovocNoTexto(nome:str):
    listaResultado = []
    listaRepetida=[]
    romper=False
    lista = []
    Listastem=[]
    listaAux2=[]
    listaCont=[]
    keywords = extraerKeywords(nome)
    #pprint(keywords)
    for n in keywords:
        romper=False
        auxiliar = aplicarStemmingLista(n.split())
        for a in auxiliar:
            Listastem.append(a[0])
        devolto=devolverNodoPoloNome(n)
        if(len(devolto)!=0):
            listaAuxiliar=[]
            listaAuxiliar.append(devolto)
            #print(listaAuxiliar)
            romper=True
            #print(listaAuxiliar)
        else:
            listaAuxiliar = StringContenLexConcepto(n)
            if(len(listaAuxiliar)==0):
                listaAuxiliar = StringContenLexConcepto(aplicarPluralFrase(n))

            #print(n)
            #print(listaAuxiliar)
            if len(listaAuxiliar)==2 and listaAuxiliar[0][0] not in listaAuxiliar[1][0] and listaAuxiliar[1][0] not in listaAuxiliar[0][0]:
                
                listaAux2=facerBusquedaDoConcepto(n)
                if(listaAux2 is not None):
                    #print(listaAux2)
                    if(len(listaAux2)>1):
                        listaAux2=[]
                        listaAux2.append(listaAuxiliar[0][0])
                    #print(listaAuxiliar[0][0])
                    #print(listaAuxiliar[1][0])
                    listaAuxiliar=[]
                    listaAuxiliar.append(devolverNodoPoloNome(listaAux2[0]))
                    #print(listaAuxiliar)
                    romper=True
                else:
                    
                    listaAux2=contidoNosConceptosSimilares(listaAuxiliar[0][0],listaAuxiliar[1][0])
                    #pprint(listaAux2)
                    if(len(listaAux2)!=0):
                        listaAuxiliar=[]
                        listaAuxiliar=(listaAux2)
                        romper=True
                    else:
                        listaAux2=contidoNosConceptosSimilares(listaAuxiliar[1][0],listaAuxiliar[0][0])
                        #pprint(listaAux2)
                        if(len(listaAux2)!=0):
                            romper=True
                            listaAuxiliar=[]
                            listaAuxiliar=(listaAux2)
        for l in listaAuxiliar:
            if romper:
                if l not in lista:
                    #print("PRODUCESE NO DE ROMPER: "+l[0])
                    lista.append(l)
                    if l not in listaResultado:
                        listaResultado.append(l)
                break
            if (len(l[0].split()) == 1):
                if (l[1]) is None:
                        if aplicarStemmingIndividual(l[0]) in Listastem:
                            if l not in lista:
                                #print(l)
                                lista.append(l)
                                contador=nome.count(lexemaTermo(l[0]))
                                l.append(contador)
                                if contador>1 and l not in listaRepetida:
                                    listaRepetida.append(l)

                else:
                    if (len(l[1].split()) == 1):
                        if aplicarStemmingIndividual(l[1]) in Listastem:
                            if l not in lista:
                                #print(l)
                                lista.append(l)
                                contador=nome.count(lexemaTermo(l[0]))
                                aux=nome.count(lexemaTermo(l[1]))
                                if(aux>contador):
                                    contador=aux
                                l.append(contador)
                                if contador>1 and l not in listaRepetida:
                                    listaRepetida.append(l)
                    else:
                        if aplicarStemmingIndividual(l[0]) in Listastem:
                            if l not in lista:
                                #print(l)
                                lista.append(l)
                                contador=nome.count(lexemaTermo(l[0]))
                                aux=nome.count(lexemaTermo(l[1]))
                                if(aux>contador):
                                    contador=aux
                                l.append(contador)
                                if contador>1 and l not in listaRepetida:
                                    listaRepetida.append(l)
            else:
                if l not in lista:
                    #print(l)
                    lista.append(l)
                    contador=nome.count(lexemaTermo(l[0]))
                    if(l[1] is not None):
                        aux=nome.count(lexemaTermo(l[1]))
                        if(aux>contador):
                            contador=aux
                    l.append(contador)
                    if contador>1 and l not in listaRepetida:
                        listaRepetida.append(l)
    
    limite=10
    contador=len(listaResultado)
    if contador >=5:
        limite=contador+5
    listaRepetida.sort(reverse=True,key=sortFunc)
    #print(listaRepetida)
    for i in listaRepetida:
       #print(i)
       if(i[3]<3):
           break
       i.pop(3)
       romper=False
       for l in listaResultado:
            if comprobarExistenciaRelacion(l[2],i[2],'Broader*')==True:
                romper=True
                print(i)
                break
            else:
                continue
        
       if i not in listaResultado and romper==False and contador<limite:
            listaResultado.append(i)
            contador+=1
    return listaResultado
def TratarTextoCientifico(titulo:str,resumo:str,uri:str):
    lista=ConceptosAgrovocNoTexto(titulo+'\n '+resumo)
    if devolverArtigo(uri) is None:
        crearArtigo(titulo,resumo,uri)
        for l in lista:
            crearClasificación(uri,l[2])
    return lista

def procesar_relacionados(nome:str,uri:str):
    relacionados =busquedaRelacionados(uri)
    #print(relacionados)
    for result in relacionados:
        if(comprobarExistencia(result[1])==False):
            crearNodo(result[0],result[1])
            procesar_alternativos(result[0],result[1])
        if(comprobarExistenciaRelacion(uri,result[1],"Relacionado")==None):
            crearRelacion(uri,result[1],"Relacionado")
def procesar_alternativos(nome:str,uri:str):
    #print("entra no proceso de alternativos")
    listaAlternativos = busquedaNomeAlternativo(uri)
    #print(listaAlternativos)
    if(len(listaAlternativos)>0):
        fixarAlcume(nome,listaAlternativos)
    lexemaEstemma(nome,listaAlternativos)
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
def TratamentoConcepto(nome,uri,pais,paiNome):
    listaParcial= []
    analizar=dividirTexto(nome.replace("'", ""))    
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
                a=getSingular(a)
                print(a)
            if(busquedaNome(a) is None):
                a=aplicarPlural(a)
                print(a)
            if(busquedaNome(a) is None):
                a = a.capitalize()
                print(a)
                #print('entrou: '+a)
            if(busquedaNome(a) is not None):
                #print('entrou2: '+a)
                nomeA,uriNome = busquedaNome(a) 
                #paiNome,pai=busquedaPai(uri)
                print(nomeA)
                #stem_nome=aplicarStemmingIndividual(nomeA)
                #palabras_stem=startsWithStem(stem_nome)
                #parar=False
                #if stem_nome in paiNome:
                    #break
                #for p in pais:
                    #if stem_nome==aplicarStemmingIndividual(p[0]):
                        #parar=True
                        #break
                #if parar==True:
                    #break
                if(comprobarXerarquia(uriNome,uri)==True):
                    break
                if(comprobarXerarquia(uri,uriNome)==True ):
                    break
                if(uriNome==uri):
                    break
                if(comprobarExistencia(uriNome)==False):
                    crearNodo(nomeA,uriNome)
                    procesar_alternativos(nomeA,uriNome)
                    procesar_relacionados(nomeA,uriNome)
                
                if(comprobarExistenciaRelacion(uriNome,uri,"Contido_en")==None):
                    print(f"nome: {nome} busquedadoPai: {paiNome} nomeA: {nomeA}")
                    crearRelacion(uriNome,uri,"Contido_en")
                
                auxiliar=[nome,uri,nomeA,uriNome]
                listaParcial.append(auxiliar) 
        return listaParcial
    else:
        return None
def TratamentoFillo(f,includeUse=False):
    #print(f)
    lista: list[str]= []
    if(comprobarExistencia(f[1])==False):
        #print(f[0])
        crearNodo(f[0],f[1])
        procesar_alternativos(f[0],f[1])
    procesar_relacionados(f[0],f[1])
    nome,uri = busquedaNome(f[0])
    
    paiNome,pai=busquedaPai(uri)
    listaPais = busquedaTodosPais(uri)
    listaIncluidos=buscarInluidos(f[1])
    listaUseOf=buscarUsedOf(f[1])
    if(includeUse==True):
        if(listaIncluidos is not None):
            #print(listaIncluidos)
            for fio in listaIncluidos:
                if(comprobarExistencia(fio[1])==False):
                    crearNodo(fio[0],fio[1])
                    procesar_alternativos(fio[0],fio[1])
                if(comprobarExistenciaRelacion(f[1],fio[1],"Narrower")==None):
                    crearRelacion(f[1],fio[1],"Narrower")
                if(comprobarExistenciaRelacion(fio[1],f[1],"Broader")==None):
                    crearRelacion(fio[1],f[1],"Broader")
                pais=busquedaPaiExhaustiva(fio[1])
                lista = TratamentoConcepto(fio[0],fio[1],pais,f[0])
                alt = busquedaNomeAlternativo(uri)
                if(len(alt)>0):
                    #print(alt)
                    for a in alt:
                        listaOcasional = TratamentoConcepto(a,uri,pais,paiNome)
        if(listaUseOf is not None):
            #print(listaUseOf)
            for fio in listaUseOf:
                if(comprobarExistencia(fio[1])==False):
                    crearNodo(fio[0],fio[1])
                    procesar_alternativos(fio[0],fio[1])
                if(comprobarExistenciaRelacion(f[1],fio[1],"Narrower")==None):
                    crearRelacion(f[1],fio[1],"Narrower")
                if(comprobarExistenciaRelacion(fio[1],f[1],"Broader")==None):
                    crearRelacion(fio[1],f[1],"Broader")
                pais=busquedaPaiExhaustiva(fio[1])
                lista = TratamentoConcepto(fio[0],fio[1],pais,f[0])
                alt = busquedaNomeAlternativo(uri)
                if(len(alt)>0):
                    #print(alt)
                    for a in alt:
                        listaOcasional = TratamentoConcepto(a,uri,pais,paiNome)
    if len(listaPais)>1:
        for fi in listaPais:
            if(comprobarExistencia(fi[1])==False):
                crearNodo(fi[0],fi[1])
                procesar_alternativos(fi[0],fi[1])
            if(comprobarExistenciaRelacion(f[1],fi[1],"Broader")==None):
                crearRelacion(f[1],fi[1],"Broader")
            if(comprobarExistenciaRelacion(fi[1],f[1],"Narrower")==None):
                crearRelacion(fi[1],f[1],"Narrower")
    
    pais=busquedaPaiExhaustiva(uri)
    #print(pais)
    #print("este e o concepto: "+f[0]+"e este é o pai: "+paiNome)
    if(comprobarExistenciaRelacion(f[1],pai,"Broader")==None):
        crearRelacion(f[1],pai,"Broader")
    if(comprobarExistenciaRelacion(pai,f[1],"Narrower")==None):
        crearRelacion(pai,f[1],"Narrower")
    lista = TratamentoConcepto(f[0],uri,pais,paiNome)
    alt = busquedaNomeAlternativo(uri)
    if(len(alt)>0):
        #print(alt)
        for a in alt:
            listaOcasional = TratamentoConcepto(a,uri,pais,paiNome)
            #print(listaOcasional)
            if listaOcasional is not None:
                #print(lista)
                if lista is None:
                    lista = listaOcasional
                else:
                    lista += listaOcasional
                #print(lista)
                
    return lista
#TratamentoFillo(['crustaceans','http://aims.fao.org/aos/agrovoc/c_eaa20250'])
def ConceptosPalabras(texto: str,inmediata=False,includes=False):
    listaNomes: list[str]= []
    nome,uri = busquedaNome(texto)
    if(comprobarExistencia(uri)==False):
        #print(nome)
        crearNodo(nome,uri)
        procesar_alternativos(nome,uri)
        procesar_relacionados(nome,uri)
    #fillos = busquedaExhaustiva(uri)
    if(inmediata==True and includes==False):
        fillos = busquedaInmediata(uri)
    elif(inmediata==False and includes==True):
        fillos=busquedaExhaustivaIncludesUse(uri)
    elif(includes==True and inmediata==True):
        fillos=busquedaInmediataIncludesUse(uri)
    else:
        fillos = busquedaExhaustiva(uri)
        
    print(f"este é o número de conceptos da mostra que imos analizar:  {len(fillos)} descendentes do seguinte concepto pai {nome}")
    for i,f in enumerate(fillos):
        print("analizamos o seguinte concepto: "+f[0]+" que se está executando no número: "+str(i)+" da orde total")
        auxiliar=TratamentoFillo(f,includeUse=includes)
        if auxiliar is not None:
            listaNomes+=auxiliar
                      
    return listaNomes

def gardarConsultaAccesos(nome: str,inmediata,includes):
    listaEscribir=ConceptosPalabras(nome,inmediata=inmediata,includes=includes)
    gardar= "csvs/"+nome + ".csv"
    #print(listaEscribir)
    cabeceira=['nome', 'uriVella',"NovoElemento","uriNiovo"]
    escribir(gardar,listaEscribir,cabeceira)
#pprint(facerBusquedaDoConcepto('chicken production'))

def gardarConceptoAmplioProximo(ascendente:str,nomeAconcatear: str):
    listaAuxiliar: list[str]= []
    listaNomes: list[str]= []
    nome,uri = busquedaNome(ascendente)
    if(comprobarExistencia(uri)==False):
        print("non se atopou o concepto para facer a busqueda")
    print(uri)
    #fillos = busquedaFillosGrafo(uri)
    fillos = busquedaExhaustiva(uri)
    print(f"este é o número de conceptos da mostra que imos analizar:  {len(fillos)} descendentes do seguinte concepto pai {nome}")
    for i,f in enumerate(fillos):
        buscado=f[0]+' '+nomeAconcatear
        print("analizamos o seguinte concepto: "+buscado+" que se está executando no número: "+str(i)+" da orde total")
        start_time = time.time()
        #auxiliar=facerBusquedaDoConcepto(buscado)
        auxiliar=facerBusqueda2Concepto(f[0],nomeAconcatear)
        tempo=round(time.time() - start_time, 2)
        listaAuxiliar.append(buscado)
        if auxiliar is not None:
            if len(auxiliar)>0:
                listaAuxiliar.append(auxiliar[0])
            else:
                listaAuxiliar.append(' ')
        else:
            listaAuxiliar.append(' ')
        listaAuxiliar.append(tempo)
        listaNomes.append(listaAuxiliar)
        #print(listaNomes)
        listaAuxiliar=[]
    gardar= "csvs/buscado"+ascendente+"_"+nomeAconcatear+"novo.csv"
    #pprint(listaNomes)
    cabeceira=['buscado','resultado','tempo']
    print(listaNomes)
    escribir(gardar,listaNomes,cabeceira)
gardarConceptoAmplioProximo('crops','agriculture')
def probaHuggingface(descende,nome):
    name,uri = busquedaNome(descende)
    fillos=busquedaExhaustivaIncludesUse(uri)
    fillos=busquedaExhaustiva(uri)
    print(fillos)
    listaAux=[]
    lista=[]
    nome,uri2 = busquedaNome(nome)
    print(uri2)
    print(nome)
    cabeceira=['nome', 'resultado','tempo']
    entrada=(descende+'_'+nome)
    gardar="csvs/probasChat/"+entrada + ".csv"
    for f in fillos:
        time.sleep(5)
        start_time = time.time()
        entrada=(f[0]+' '+nome)
        listaAux.append(entrada)
        print(entrada)
        mensaxe=funcionchat(entrada,uri2)
        print(mensaxe)
        listaAux.append(mensaxe)
        listaAux.append(round(time.time() - start_time, 2))
        lista.append(listaAux)
        listaAux=[]
    escribir(gardar,lista,cabeceira)
#probaHuggingface('useful animals','housing')
def gardadoXeralConsultaAccesos():
    listaEscribir: list[str]= []
    listaInicial=busquedaOrfos()
    cabeceira=['nome', 'uriVella',"NovoElemento","uriNiovo"]
    
    for l in listaInicial:
        listaEscribir=[]
        gardar="csvs/"+l[0] + ".csv"
        print(f"\n IMOS EXPLORAR AGORA ESTE CONCEPTO INICIAL: {l[0]} \n")
        if l[0] == 'organisms': 
            if os.path.exists("csvs/pests.csv") :
                continue
            else:
                gardarConsultaAccesos("useful animals",False,True)
                gardarConsultaAccesos("plants",False,False)
                gardarConsultaAccesos("pests",False,False)
                gardarConsultaAccesos("insects",False,False)
                gardarConsultaAccesos("animals",True,False)
                gardarConsultaAccesos("invertebrates",True,False)
                gardarConsultaAccesos("organisms",True,False)
                continue
        if os.path.exists(gardar) :
            continue
        listaEscribir=ConceptosPalabras(l[0])
       
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