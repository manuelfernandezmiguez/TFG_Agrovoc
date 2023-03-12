import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
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

#print(aplicarPlural("calf"))