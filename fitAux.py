import math

def elitismo(fit):

    POP = len(fit)
    
    eliteInd = -1
    melhorFit = -100
    
    for i in range(0, POP):
        if(fit[i] > melhorFit):
            eliteInd = i
            melhorFit = fit[i]
    
    return eliteInd

def elitismoMin(fit):

    POP = len(fit)
    
    eliteInd = -1
    melhorFit = 90000000
    
    for i in range(0, POP):
        if(fit[i] < melhorFit):
            eliteInd = i
            melhorFit = fit[i]
    
    return eliteInd
    
def melhorFitFunc(fit, max):
    
    if(max == True):
        maiorInd = elitismo(fit)
    else:
        maiorInd = elitismoMin(fit)
    
    return fit[maiorInd]
    
def mediaFit(fit):
    
    POP = len(fit)
    
    total = 0.0
    for i in fit:
        total = total + i
    
    return (total/POP)

def desvioPadraoFit(fit, media, pop):

    soma = 0
    
    for i in fit:
        soma += ((i - media)**2)
    soma = soma/pop
    
    return math.sqrt(soma)
    