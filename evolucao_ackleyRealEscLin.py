# gerar uma população inicial
# indivíduos binários, inteiros ou reais
# BIN, INT, REAL
# tam. população: POP
# tam. cromossomo: D
# domínio: [Li, Ui]

# random: Mersenne Twister



import time
import random
import math
import sys
import copy

import leitura
import populacao
import diversidade
import binConv
import selecEscLin
import crossover
import mutacao
import fitAux


'''
funções:
gerar listas aleatórias:
geraMatrizBin(POP, D)
geraMatrizInt(POP, D, Li, Ui, permutável)
geraMatrizReal(POP, D, Li, Ui)

'''


'''
Implementar: função ackley, duas dimensões, duas casas decimais, codificação binária
domínio: [-32,32] -> 65 valores inteiros -> 6500 valores de duas casas decimais -> 13 bits!

'''

######## loop evolutivo

def rotinaEvolucao(arqEnt, arqEvol):

    TIPO, POP, D, Li, Ui, extra = leitura.entrada(arqEnt)
    sel, elite, cxTipo, cxProb, mutProb, passos, nExec = leitura.paramEvo(arqEvol)
    arqFit = open('fitness.txt', 'w')
    arqDivPar = open('diversidadePar.txt', 'w')
    arqDivCentro = open('diversidadeCentro.txt', 'w')
    
    melhorFitLista = [0.0]*passos
    mediaFitLista = [0.0]*passos
    divParLista = [0.0]*passos
    divCentroLista = [0.0]*passos
    
    max = False
    if(max == True):
        melhorFit = -100.0
    else:
        melhorFit = 9000000.0
    
    for i in range(0, nExec):
        melhorIndAtual, melhorFitAtual = evolui(TIPO, POP, D, Li, Ui, extra, sel, elite, cxTipo, cxProb, mutProb, passos, melhorFitLista, mediaFitLista, divParLista, divCentroLista)
        if(max == True and melhorFitAtual > melhorFit):
            melhorFit = melhorFitAtual
            melhorInd = copy.deepcopy(melhorIndAtual)
        elif(max == False and melhorFitAtual < melhorFit):
            melhorFit = melhorFitAtual
            melhorInd = copy.deepcopy(melhorIndAtual)
    
    for i in range(0, passos):
        melhorFitLista[i] = melhorFitLista[i]/nExec
        mediaFitLista[i] = mediaFitLista[i]/nExec
        divParLista[i] = divParLista[i]/nExec
        divCentroLista[i] = divCentroLista[i]/nExec
        
        s = '{} {} {}\n'.format(i, melhorFitLista[i], mediaFitLista[i])
        arqFit.write(s)
        
        s = '{} {}\n'.format(i, divParLista[i])
        arqDivPar.write(s)
        
        s = '{} {}\n'.format(i, divCentroLista[i])
        arqDivCentro.write(s)
    
    result = ackleyInd(melhorInd)   ###### função ackley
    
    return melhorInd, result
    
def evolui(TIPO, POP, D, Li, Ui, extra, sel, elite, cxTipo, cxProb, mutProb, passos, melhorFitLista, mediaFitLista, divParLista, divCentroLista):
    
    matriz = populacao.geraPop(TIPO, POP, D, Li, Ui, extra)
    fit = ackleyPop(matriz) ##### função ackley
    max = False  #### minimizar ou maximizar
    
    i = 0
    maior = fitAux.melhorFitFunc(fit, max)
    media = fitAux.mediaFit(fit)
    #s = '{} {} {}\n'.format(i, maior, media)
    #arqFit.write(s)
    melhorFitLista[i] += maior
    mediaFitLista[i] += media
    
    divPar = diversidade.diversidadePar(TIPO, matriz, Li, Ui)
    divCentro = diversidade.diversidadeCentro(TIPO, matriz, Li, Ui)
    #s = '{} {} {}\n'.format(i, divPar, divCentro)
    #arqDiv.write(s)
    divParLista[i] += divPar
    divCentroLista[i] += divCentro
    
    melhorFitTotal = maior
    melhorIndTotal = copy.deepcopy(matriz[fitAux.elitismo(fit)])
    
    c = 1.2
    passosCrescer = selecEscLin.cPassosCrescer(passos, 0.2)
    for i in range(1, passos):      
        
        if(elite == True and max == True):
            eliteInd = fitAux.elitismo(fit)
            eliteCod = copy.deepcopy(matriz[eliteInd])
        elif(elite == True and max == False):
            eliteInd = fitAux.elitismoMin(fit)
            eliteCod = copy.deepcopy(matriz[eliteInd])
        
        sl = selecEscLin.selecao(matriz, fit, POP, sel, max, c)
        cross = crossover.rotinaCrossOver(sl, TIPO, extra, cxTipo, cxProb, Li, Ui)
        mut = mutacao.rotinaMutacao(cross, TIPO, extra, mutProb, Li, Ui)
        
        c = selecEscLin.aumentaC(c, i, passosCrescer)
        
        if(elite == True):
            sub = random.randrange(0, POP)
            mut[sub] = eliteCod
        
        matriz = copy.deepcopy(mut)
        fit = ackleyPop(matriz) ##### função ackley
        
        maior = fitAux.melhorFitFunc(fit, max)
        media = fitAux.mediaFit(fit)
        #s = '{} {} {}\n'.format(i, maior, media)
        #arqFit.write(s)
        melhorFitLista[i] += maior
        mediaFitLista[i] += media
        
        divPar = diversidade.diversidadePar(TIPO, matriz, Li, Ui)
        divCentro = diversidade.diversidadeCentro(TIPO, matriz, Li, Ui)
        #s = '{} {} {}\n'.format(i, divPar, divCentro)
        #arqDiv.write(s)
        divParLista[i] += divPar
        divCentroLista[i] += divCentro
        
        if(max == True and maior > melhorFitTotal):
            melhorIndTotal = copy.deepcopy(matriz[fitAux.elitismo(fit)])
            melhorFitTotal = maior
        elif(max == False and maior < melhorFitTotal):
            melhorIndTotal = copy.deepcopy(matriz[fitAux.elitismoMin(fit)])
            melhorFitTotal = maior
    
    #melhorInt, result = pesResultadoIndiv(melhorIndTotal, D, Li, Ui, extra)   ###### função da fábrica de rádios
    
    return melhorIndTotal, melhorFitTotal
    
########
  

def ackleyInd(chromosome):
    #http://www.cs.unm.edu/~neal.holts/dga/benchmarkFunction/ackley.html
    
    firstSum = 0.0
    secondSum = 0.0
    
    for c in chromosome:
        firstSum += c**2.0
        secondSum += math.cos(2.0*math.pi*c)
    n = float(len(chromosome))
    
    return -20.0*math.exp(-0.2*math.sqrt(firstSum/n)) - math.exp(secondSum/n) + 20 + math.e

def ackleyIndBin(indiv, D, Li, Ui, extra):

    iReal = binConv.converteBin([indiv], D, Li, Ui, extra)
    
    res = ackleyInd(iReal[0])
    
    return iReal, res

def ackleyPop(matriz):

    fit = []
    POP = len(matriz)
    
    for i in range(0, POP):
        fit.append(ackleyInd(matriz[i]))
    
    return fit

def ackleyPopBin(matriz, D, Li, Ui, extra):
    
    mInt = binConv.converteBin(matriz, D, Li, Ui, extra)
    
    fit = []
    POP = len(mInt)
    
    for i in range(0, POP):
        fit.append(ackleyInd(mInt[i]))
    
    return fit
    
    
########


random.seed(time.time())

arqEnt = 'paramPop.txt'
arqEvol = 'paramEvol.txt'

melhorInd, result = rotinaEvolucao(arqEnt, arqEvol)
#restricoes = avaliaRestricoes(melhorInd)


print("Melhor indivíduo:")
print(melhorInd)
print()
#print("Melhor indivíduo real:")
#print(melhorIndReal)
#print()
#print("[standard, luxo]:")
#print(melhorInt[0])
print()
print("Função Ackley aplicada ao melhor indivíduo:")
print(result)
print()
#print("Restrições:")
#print(restricoes)


#teste = ([0.2,0.0,0.1], [0.8, 0.9, 0.3])
#teste = ([1,2,3,4,5,6,7,8], [5,3,2,6,1,8,7,4])
#Li = [-1.0, -1.0, -1.0]
#Ui = [1.0, 1.0, 1.0]
#teste = ([0.3, 1.4, 0.2, 7.4], [0.5, 4.5, 0.1, 5.6])
#n1, n2 = cxPMX(teste[0], teste[1], 1)
#mutPerm(teste, 0.5)
#print(teste)
#print(teste[0])
#print(teste[1])
#print()
#print(n1)
#print(n2)



