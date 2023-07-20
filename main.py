from xeneral import gardarConsultaAccesos, explorar,gardadoXeralConsultaAccesos,gardarConceptoAmplioProximo

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

def op3():
    gardadoXeralConsultaAccesos()

def op4():
    print("esta é a cuarta opción")
    print("Introduza os dous elementos para buscar todos os ancestros comúns a todos os descendentes do primeiro nome mais o segundo:")
    nome=str(input())
    nome2=str(input())
    gardarConceptoAmplioProximo(nome,nome2)

mensaxe= '''
Estas son todas as opcións posibles:
0 Saír
1 Imprimir xerarquía
2 Obter excel
3 almacear todos os datos e xerar os excels
4 usar dous conceptos para ver como vai a funcion facerBuscadoConcepto cos fillos do primeiro concepto e mais o segundo concepto

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
    elif(opt==3):
        op3()
    elif(opt==4):
        op4()
    else:
        print("esa opción non está contemplada")
