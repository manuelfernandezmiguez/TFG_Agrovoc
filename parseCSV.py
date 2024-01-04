import csv

def escribir(nomeFicheiro: str,listaDatos,cabeceira):
    with open(nomeFicheiro, mode='w',newline='') as folla:
        escritor = csv.DictWriter(folla, fieldnames=cabeceira)
        escritor.writeheader()
        for l in listaDatos:
            datos = {cabeceira[i]: l[i] for i in range(len(cabeceira))}
            print(datos)
            escritor.writerow(datos)
        