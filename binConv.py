import math

def converteBin(matriz, D, Li, Ui, extra):
    
    if(extra == 'INT'):
        nova = converteInt(matriz, D, Li, Ui)
    else:
        nova = converteReal(matriz, D, Li, Ui, extra[1])
    
    return nova

def converteBinRealGene(gene, Li, Ui, prec):

    valor = 0
    tam = len(gene)
    
    for i in range(0, tam):
        valor = valor + (int(gene[i]))*(2**(tam-1-i))
    
    intervalo = (math.ceil(Ui) - math.floor(Li) + 1)*(10**prec)
    bits = intervalo.bit_length()
    fConv = (Ui - Li)/((2**bits)-1)
    
    real = Li + fConv*valor
    real = round(real, prec)
    
    return real
    
def converteReal(matriz, D, Li, Ui, prec):

    #tam = int(len(matriz[0])/D)
    POP = len(matriz)
    
    matConv = []
    for i in range(0, POP):
        indiv = []
        atual = 0
        for j in range(0, D):
            intervalo = (math.ceil(Ui[j]) - math.floor(Li[j]) + 1)*(10**prec)
            tamGene = intervalo.bit_length()
            gene = converteBinRealGene(matriz[i][atual:atual+tamGene], Li[j], Ui[j], prec)
            indiv.append(gene)
            atual = atual + tamGene
        matConv.append(indiv)
    
    return matConv

def converteBinIntGene(gene, Li, Ui):

    valor = 0
    tam = len(gene)
    
    for i in range(0, tam):
        valor = valor + (int(gene[i]))*(2**(tam-1-i))
    
    intervalo = int(Ui) - int(Li) + 1
    bits = intervalo.bit_length()
    fConv = (Ui - Li)/((2**bits)-1)
    
    inte = Li + fConv*valor
    inte = int(round(inte))
    
    return inte
    
def converteInt(matriz, D, Li, Ui):

    #tam = int(len(matriz[0])/D)
    POP = len(matriz)
    
    matConv = []
    for i in range(0, POP):
        indiv = []
        atual = 0
        for j in range(0, D):
            intervalo = int(Ui[j]) - int(Li[j]) + 1
            tamGene = intervalo.bit_length()
            gene = converteBinIntGene(matriz[i][atual:atual+tamGene], Li[j], Ui[j])
            indiv.append(gene)
            atual = atual + tamGene
        matConv.append(indiv)
    
    return matConv  