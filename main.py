from xeneral import gardarConsultaAccesos, explorar

def op1():
    print("esta é a primeira opción")
    print("Introduza o elemento a representar:")
    nome=str(input())
    explorar(nome)

def op2():
    print("esta é a segunda opción")
    print("Introduza o elemento a buscar:")
    nome=str(input())
    gardarConsultaAccesos(nome)

mensaxe= '''
Estas son todas as opcións posibles:
0 Saír
1 Imprimir xerarquía
2 Obter excel

Introduce a opción que queres:
'''



opt = -1
while(opt!=0):
    print(mensaxe)
    opt=int(input())
    if(opt==0):
        break
    elif(opt==1):
        op1()
    elif(opt==2):
        op2()
    else:
        print("esa opción non está contemplada")
