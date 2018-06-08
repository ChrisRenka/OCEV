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
import copy

import leitura
import populacao
import diversidade
import binConv
import selec
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
    #cidades = geraCidades(D)
    cidades = cidadesComum()
    
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
        melhorIndAtual, melhorFitAtual = evolui(TIPO, POP, D, Li, Ui, extra, sel, elite, cxTipo, cxProb, mutProb, passos, melhorFitLista, mediaFitLista, divParLista, divCentroLista, cidades)
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
    
    result = fitIndivTSM(melhorInd, cidades) ##### caixeiro viajante
    
    return melhorInd, result, cidades
    
def evolui(TIPO, POP, D, Li, Ui, extra, sel, elite, cxTipo, cxProb, mutProb, passos, melhorFitLista, mediaFitLista, divParLista, divCentroLista, cidades):
    
    matriz = populacao.geraPop(TIPO, POP, D, Li, Ui, extra)
    fit = fitPopTSM(matriz, cidades) ##### caixeiro viajante
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
    
    for i in range(1, passos):      
        
        if(elite == True and max == True):
            eliteInd = fitAux.elitismo(fit)
            eliteCod = copy.deepcopy(matriz[eliteInd])
        elif(elite == True and max == False):
            eliteInd = fitAux.elitismoMin(fit)
            eliteCod = copy.deepcopy(matriz[eliteInd])
        
        sl = selec.selecao(matriz, fit, POP, sel, max)
        cross = crossover.rotinaCrossOver(sl, TIPO, extra, cxTipo, cxProb, Li, Ui)
        mut = mutacao.rotinaMutacao(cross, TIPO, extra, mutProb, Li, Ui)
        
        if(elite == True):
            sub = random.randrange(0, POP)
            mut[sub] = eliteCod
        
        matriz = copy.deepcopy(mut)
        fit = fitPopTSM(matriz, cidades) ##### caixeiro viajante
        
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
  
def geraCidades(D):

    cidades = []
    
    for i in range(0, D):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        cidades.append([x,y])
    
    return cidades

def cidadesComum():

    c = [[0.00, 0.20], [0.15, 0.80], [0.20, 0.65], [0.90, 0.30], [0.75, 0.45], [0.30, 0.75], [0.05, 0.05], [0.95, 0.95], [0.55, 0.55], [0.85, 0.25]]

    return c
    
def fitIndivTSM(indiv, cidades):

    fit = 0.0
    D = len(indiv)
    
    for i in range(0, D-1):
        dist = math.sqrt(((cidades[indiv[i]][0] - cidades[indiv[i+1]][0])**2) + ((cidades[indiv[i]][1] - cidades[indiv[i+1]][1])**2) )
        fit += dist
    dist = math.sqrt(((cidades[indiv[D-1]][0] - cidades[indiv[0]][0])**2) + ((cidades[indiv[D-1]][1] - cidades[indiv[0]][1])**2) )
    fit += dist
    
    return fit

def fitPopTSM(matriz, cidades):

    POP = len(matriz)
    fit = []
    
    for i in range(0, POP):
        fit.append( fitIndivTSM(matriz[i], cidades) )
    
    return fit

def gravaCaminho(indiv, cidades):

    arq = open('percurso.txt', 'w')
    D = len(indiv)
    
    for i in range(0, D):
        s = '{} {}\n'.format(cidades[indiv[i]][0], cidades[indiv[i]][1])
        arq.write(s)
    s = '{} {}\n'.format(cidades[indiv[0]][0], cidades[indiv[0]][1])
    arq.write(s)
    
    
########


random.seed(time.time())

arqEnt = 'paramPop.txt'
arqEvol = 'paramEvol.txt'

melhorInd, result, cidades = rotinaEvolucao(arqEnt, arqEvol)
#restricoes = avaliaRestricoes(melhorInd)
gravaCaminho(melhorInd, cidades)

print("Melhor indivíduo:")
print(melhorInd)
print()
#print("Melhor indivíduo real:")
#print(melhorIndReal)
#print()
#print("[standard, luxo]:")
#print(melhorInt[0])
print("Comprimento do menor percurso encontrado:")
print(result)
print()
#print("Restrições:")
#print(restricoes)


#teste = ([0,1,2,3,4,5,6,7,8,9], [9,8,7,6,5,4,3,2,1,0])
#testeCid = geraCidades(10)
#print(testeCid)
#fit = fitPopTSM(teste, testeCid)
#print(fit)
#gravaCaminho(teste[0], testeCid)



