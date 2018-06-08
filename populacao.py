import math
import random

def geraPop(TIPO, POP, D, Li, Ui, extra):
    
    if(TIPO == 'BIN'):
        if(extra == True or extra == False):
            matriz = geraMatrizBin(POP, D)
        else:
            matriz = geraMatrizBinConv(POP, D, Li, Ui, extra)
    elif(TIPO == 'REAL'):
        matriz = geraMatrizReal(POP, D, Li, Ui)
    else:
        matriz = geraMatrizInt(POP, D, Li, Ui, extra)
    
    return matriz

def geraMatrizBin(POP, D):

	matriz = []
	
	for i in range(0, POP):
	    indiv = []
	    for j in range(0, D):
	        indiv.append(random.choice([True, False]))
	    matriz.append(indiv)
	
	return matriz
    
def geraMatrizBinConv(POP, D, Li, Ui, extra):
    
    if(extra == 'INT'):
        #total = int(Ui) - int(Li) + 1
        #bits = D*(total.bit_length())
        bits = 0
        for i in range(0, D):
            total = int(Ui[i]) - int(Li[i]) + 1
            bits = bits + (total.bit_length())
    else:
        #sup = math.ceil(Ui)
        #inf = math.floor(Li)
        #total = (sup - inf + 1)*(10**extra[1])
        #bits = D*(total.bit_length())
        bits = 0
        for i in range(0, D):
            sup = math.ceil(Ui[i])
            inf = math.floor(Li[i])
            total = (sup - inf + 1)*(10**extra[1])
            bits = bits + (total.bit_length())
    
    matriz = geraMatrizBin(POP, bits)
    
    return matriz
    
def geraMatrizReal(POP, D, Li, Ui):

    matriz = []
    
    for i in range(0, POP):
        indiv = []
        for j in range(0, D):
            indiv.append(random.uniform(Li[j], Ui[j]))
        matriz.append(indiv)
    
    return matriz

def geraMatrizInt(POP, D, Li, Ui, P):
    
    if(P==False):    
        matriz = geraMatrizIntNPerm(POP, D, Li, Ui)
    else:
        matriz = geraMatrizIntPerm(POP, Li, Ui)
    
    return matriz

def geraMatrizIntNPerm(POP, D, Li, Ui):

    matriz = []
    
    for i in range(0, POP):
        indiv = []
        for j in range(0, D):
            indiv.append(random.randrange(Li[j], Ui[j]+1))
        matriz.append(indiv)
    
    return matriz
    
def geraMatrizIntPerm(POP, Li, Ui):

    matriz = []
    
    for i in range(0,POP):
        indiv = random.sample(range(Li[0], Ui[0]+1), Ui[0] - Li[0] + 1)
        matriz.append(indiv)
    
    return matriz
    
def printPop(matriz, tipo):

    POP = len(matriz)
    
    for i in range(0, POP):
        if(tipo != 'REAL'):
            print(matriz[i])
        else:
            a = []
            for j in matriz[i]:
                a.append(round(j, 3))
            print(a)