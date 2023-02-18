import nltk
from nltk.tokenize import word_tokenize




def dividirTexto(text: str):
    devolver=word_tokenize(text)
    return devolver

def dividirTextoListas(lista: list):
    listaDevolver: list[str]= []
    for l in lista:
        listaDevolver.append(word_tokenize(l))
    return listaDevolver


#devolver = dividirTexto("guinea fowl")
#print(devolver[1])
