from sparqlQueries import busqueda,busquedaNome
from pprint import pprint

def explorar(nome: str):
    qres = busquedaNome(nome)
    pprint(qres)

print("¿Cómo se llama?")
nome = input()
explorar(nome)
#busqueda('http://aims.fao.org/aos/agrovoc/c_6145')
#busquedaNome('water')