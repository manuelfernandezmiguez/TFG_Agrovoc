import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import inflect

def dividirTexto(text: str):
    devolver=word_tokenize(text)
    return devolver

def dividirTextoListas(lista: list):
    listaDevolver: list[str]= []
    for l in lista:
        listaDevolver.append(word_tokenize(l))
    return listaDevolver

def aplicarStemming(string):
    ps = PorterStemmer()
    lista = []
    words = word_tokenize(string)
    
    for w in words:
        lista.append(ps.stem(w))
    #print(lista)
    return lista

def aplicarStemmingIndividual(palabra):
    ps = PorterStemmer()
    return ps.stem(palabra)
#print(aplicarStemming("Programmers program with programming languages"))

def aplicarPlural(nome):
    m = inflect.engine()
    return m.plural(nome)

def estaEnIngles(string):

    for i in dividirTexto(string):
        if not wordnet.synsets(i):
        #Not an English Word
            continue
        else:
            return True
            #se polo menos unha palabra está en inglés significará que non é un termo en latin, devolvemos true
        #English Word
    #se ningunha pertence ao vocabulario inglés devolvemos false
    return False    

#print(aplicarPlural("calf"))
#estaEnIngles("pinus radiata")
#print(estaEnIngles("Argentinian duck"))
