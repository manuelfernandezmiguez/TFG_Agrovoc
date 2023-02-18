import csv

def escribir(nomeFicheiro: str,listaDatos,cabeceira):
    with open(nomeFicheiro, mode='w') as folla:
        escritor = csv.DictWriter(folla, fieldnames=cabeceira)
        escritor.writeheader()
        for l in listaDatos:
            datos = {cabeceira[i]: l[i] for i in range(len(cabeceira))}
            escritor.writerow(datos)
        