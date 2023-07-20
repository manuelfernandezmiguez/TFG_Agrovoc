import nltk
import pprint
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import inflect
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
import spacy  # version 3.5
import en_core_web_sm
nlp = en_core_web_sm.load()
nlp.add_pipe("entityLinker", last=True)
rake_nltk_var = Rake(min_length=2, max_length=8,include_repeated_phrases=True)
inflectEngine = inflect.engine()
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def getSingular(word):
    return word if not inflectEngine.singular_noun(word) else inflectEngine.singular_noun(word)


def dividirTexto(text: str):
    devolver=word_tokenize(text)
    return devolver

def dividirTextoListas(lista: list):
    listaDevolver: list[str]= []
    for l in lista:
        listaDevolver.append(word_tokenize(l))
    return listaDevolver
def aplicarStemming(string):
    
    lista = []
    words = word_tokenize(string)
    
    for w in words:
        lista.append(ps.stem(w))
    #print(lista)
    return lista
def aplicarStemmingLista(lista:list):
    listaDevolver = []
    for l in lista:
        listaDevolver.append(aplicarStemming(l))
    return listaDevolver
#print(aplicarStemmingLista(['two cats','three cats','four cats']))
def aplicarStemmingIndividual(palabra):
    
    return ps.stem(palabra)
#print(aplicarStemming("Programmers program with programming languages"))
#print(', '.join(aplicarStemming("Programmers program with programming languages")))

def aplicarPlural(nome):

    return inflectEngine.plural(nome)

def aplicarPluralFrase(frase:str):
    devolver:str = ''
    for f in frase.split():
        devolver+=aplicarPlural(f)+' '
    return devolver
#print(aplicarPluralFrase("i have a beehive"))
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

def extraerKeywords(text:str):
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    return keyword_extracted
#print(extraerKeywords('We present a fully automatic online video system, which is able to detect the behaviour of honeybees at the beehive entrance. Our monitoring system focuses on observing the honeybees as naturally as possible (i.e. without disturbing the honeybees). It is based on the Raspberry Pi that is a low-cost embedded computer with very limited computational resources as compared to an ordinary PC. The system succeeds in counting honeybees, identifying their position and measuring their in-and-out activity. Our algorithm uses background subtraction method to segment the images. After the segmentation stage, the methods are primarily based on statistical analysis and inference. The regression statistics (i.e. ) of the comparisons of system predictions and manual counts are 0.987 for counting honeybees, and 0.953 and 0.888 for measuring in-activity and out-activity, respectively. The experimental results demonstrate that this system can be used as a tool to detect the behaviour of honeybees and assess their state in the beehive entrance. Besides, the result of the computation time show that the Raspberry Pi is a viable solution in such real-time video processing system.'+' Automatic behaviour analysis system for honeybees using computer vision'))
#print(aplicarPlural("calf"))
#estaEnIngles("pinus radiata")
#print(estaEnIngles("Argentinian duck"))

def lexemaTermo(word):

    base_word = lemmatizer.lemmatize(word, pos='n')
    base_word2 = lemmatizer.lemmatize(word, pos='a')
    base_word3 = lemmatizer.lemmatize(word, pos='v')
    if base_word3 != word:
        #print("1")
        return base_word3
    if base_word2 != word:
        #print("2")
        return base_word2
    else:
        #print("3")
        return base_word
def lexemaConcepto(lista:str):
    devolto=[]
    for w in word_tokenize(lista):
        devolto.append(lexemaTermo(w))
    return devolto
def lexemaLista(lista:list):
    listaDevolver:list = []
    for l in lista:
        listaDevolver.append(lexemaConcepto(l))
    return listaDevolver
#print(lexemaLista(['anual malnutritions','falling rocks','bookshop corpora','better job']))
#print(lexemaTermo('malnutritions'))
#print(lexemaTermo('rocks'))
#print(lexemaTermo('corpora'))
#print(lexemaTermo('better'))
def combinacionParaBusqueda(nome:str):
    devolver=word_tokenize(nome)
    lista = []
    listaDevolver = []
    lista.append(nome)
    anterior=""
    conjunto=""
    if ')' in nome:
        lista = nome.split(') ')
        lista[0]=lista[0]+')'
        return lista
    for palabra in devolver:
        lista.append(palabra)
        lista.append(getSingular(palabra))
        lista.append(inflectEngine.plural(palabra))
        if(anterior!=""):
            lista.append(anterior+" "+inflectEngine.plural(palabra))
            lista.append(anterior+" "+getSingular(palabra))
            lista.append(inflectEngine.plural(anterior)+" "+palabra)
            lista.append(getSingular(anterior)+" "+palabra)
            lista.append(anterior+" "+palabra)
            if(conjunto==""):
                conjunto=anterior+" "+palabra
            else:
                conjunto=conjunto+" "+palabra
                lista.append(conjunto)
                
        anterior = palabra
    for l in lista:
        if l not in listaDevolver:
            listaDevolver.append(l)
    #print(listaDevolver)
    return listaDevolver

#print(combinacionParaBusqueda("drones (insects) housing"))
#print(lexemaTermo("fishing"))
def devolverConceptosWikidata(texto:str):
    doc = nlp(texto)
    all_linked_entities = doc._.linkedEntities
    return all_linked_entities



