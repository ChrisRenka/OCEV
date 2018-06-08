import random
import copy
import sys
import math

def maiorFit(fit):
    
    melhorFit = -100
    
    for i in fit:
        if(i > melhorFit):
            melhorFit = i
    
    return melhorFit
    
def mediaFit(fit):
    
    total = 0.0
    for i in fit:
        total = total + i
    
    POP = len(fit)
    
    return (total/POP)

def minFit(fit):

    menorFit = 100000
    
    for i in fit:
        if(i < menorFit):
            menorFit = i
    
    return menorFit
    
def escalonaFit(fit, c):

    menor = minFit(fit)
    media = mediaFit(fit)
    maior = maiorFit(fit)
    
    if(menor == maior):
        fitEs = copy.deepcopy(fit)
        return fitEs
        
    comp = ((c*media)-maior)/(c-1)
    
    if(menor > comp):
        a = (media*(c-1))/(maior-media)
        b = (media*(maior-c*media))/(maior-media)
    else:
        a = media/(media-menor)
        b = (-menor*media)/(media-menor)
    
    
    fitEs = []
    for i in fit:
        fitEs.append((a*i) + b)
    
    return fitEs

def cPassosCrescer(passos, p):

    final = passos*p
    return (passos - final)

def aumentaC(c, i, pCresce):

    if(i < pCresce):
        return c + 0.8/pCresce
    return c

def roleta(fitness, total):

    POP = len(fitness)
    prob = random.uniform(0, 1)
    if(total == 0):
        print('Erro na seleção por roleta: total incorreto')
        sys.exit()
    
    acum = 0.0
    for i in range(0, POP):
        acum = acum + (fitness[i]/total)
        if(acum > prob):
            return i
    
    print("Erro na seleção por roleta: indivíduo não encontrado")
    sys.exit()

def roletaTotal(fitness):
    
    POP = len(fitness)
    
    total = 0.0
    for i in range(0, POP):
        total = total + fitness[i]
        
    return total

def inverteFit(fitness):
    
    tam = len(fitness)
    fator = 1.15
    maior = fator*(maiorFit(fitness))
    fitInv = []
    
    for i in range(0, tam):
        fitInv.append(maior - fitness[i])
    
    return fitInv

def torneio(fitness, k):

    #fitTemp = copy.deepcopy(fitness)
    POP = len(fitness)
    maior = -10.0
    maiorInd = -1
    
    fitTemp = []
    for i in range(0, POP):
        fitTemp.append([fitness[i], i])
    
    for i in range(0, k):
        t = random.randrange(0, POP)
        if(fitTemp[t][0] > maior):
            maior = fitTemp[t][0]
            maiorInd = fitTemp[t][1]
        fitTemp.pop(t)
        POP = POP - 1
    
    if(maiorInd != -1):
        return maiorInd
    print("Erro na seleção por torneio")
    sys.exit()

def torneioMin(fitness, k):

    POP = len(fitness)
    menor = 90000000.0
    menorInd = -1
    
    fitTemp = []
    for i in range(0, POP):
        fitTemp.append([fitness[i], i])
    
    for i in range(0, k):
        t = random.randrange(0, POP)
        if(fitTemp[t][0] < menor):
            menor = fitTemp[t][0]
            menorInd = fitTemp[t][1]
        fitTemp.pop(t)
        POP = POP - 1
    
    if(menorInd != -1):
        return menorInd
    print("Erro na seleção por torneio")
    sys.exit()
    
def rotinaSelecao(fit, sel, max, total):
    
    if(sel == 0):
        if(total[0] == 0):
            total[0] = roletaTotal(fit)
        ind1 = roleta(fit, total[0])
        ind2 = roleta(fit, total[0])
    else:
        if(max == True):
            ind1 = torneio(fit, sel)
            ind2 = torneio(fit, sel)
        else:
            ind1 = torneioMin(fit, sel)
            ind2 = torneioMin(fit, sel)
    
    return ind1, ind2
    
def selecao(matriz, fit, POP, sel, max, c, g):
    
    gap, tamPop = genGap(matriz, fit, POP, g)
    
    selec = []
    total = [0]
    if(max == False and sel == 0):
        temp = inverteFit(fit)
        atual = escalonaFit(temp, c)
    elif(sel == 0):
        atual = escalonaFit(fit, c)
    else:
        atual = copy.deepcopy(fit)
    
    for i in range(0, int(tamPop/2)):
        ind1, ind2 = rotinaSelecao(atual, sel, max, total)
        
        selec.append(matriz[ind1])
        selec.append(matriz[ind2])
    
    #print(teste)
    return selec, gap
    
def genGap(matriz, fit, POP, g):
    
    if(g == 1.0):
        return [], POP
    
    totalSelec = int(POP*g)
    if(totalSelec%2 == 1):
        totalSelec += 1
    totalGap = POP - totalSelec
    
    tamPop = POP
    matrizGap = []
    for i in range(0, totalGap):
        r = random.randrange(0, tamPop)
        matrizGap.append(copy.deepcopy(matriz[r]))
        matriz.pop(r)
        fit.pop(r)
        tamPop -= 1
    
    return matrizGap, tamPop

def genGapPasso(genMax):

    return int(genMax/6)

def genGapNovo(g, gen, genMax, genPasso):

    if(gen%genPasso == 0):
        return min(g + 0.1, 1.0)
    return g






