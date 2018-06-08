import random
import copy
import sys

def maiorFit(fit):

    POP = len(fit)
    
    melhorFit = -100
    
    for i in range(0, POP):
        if(fit[i] > melhorFit):
            melhorFit = fit[i]
    
    return melhorFit

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
    
def selecao(matriz, fit, POP, sel, max):

    selec = []
    #teste = []
    total = [0]
    if(max == False and sel == 0):
        atual = inverteFit(fit)
    else:
        atual = copy.deepcopy(fit)
    
    for i in range(0, int(POP/2)):
        #atual = copy.deepcopy(fit)
        #total = [0]
        ind1, ind2 = rotinaSelecao(atual, sel, max, total)
        #atual.pop(ind1)
        
        #ind2 = rotinaSelecao(atual, sel)
        #if(ind2 >= ind1):
        #    ind2 = ind2 + 1
        
        selec.append(matriz[ind1])
        selec.append(matriz[ind2])
        
        #teste.append(ind1)
        #teste.append(ind2)
    
    #print(teste)
    return selec
