import copy
import random

def inverte(t):
    
    if(t == True):
        return False
    return True

def mutBin(ind, prob):

    tam = len(ind)
    
    for i in range(0, tam):
        p = random.uniform(0, 1)
        if(p < prob):
            ind[i] = inverte(ind[i])

def mutIntNPerm(ind, prob, Li, Ui):

    tam = len(ind)
    
    for i in range(0, tam):
        p = random.uniform(0, 1)
        if(p < prob):
            n = random.randrange(Li[i], Ui[i]+1)
            ind[i] = n

def mutDelta(ind, prob, Li, Ui):

    tam = len(ind)
    
    for i in range(0, tam):
        p = random.uniform(0, 1)
        if(p < prob):
            s = random.choice([0,1])
            u = random.uniform(Li[i], Ui[i])
            u = u/10.0
            if(s == 0):
                ind[i] = ind[i] - u
                if(ind[i] < Li[i]):
                    ind[i] = Li[i]
            else:
                ind[i] = ind[i] + u
                if(ind[i] > Ui[i]):
                    ind[i] = Ui[i]

def mutGauss(ind, prob, Li, Ui):

    tam = len(ind)
    #sd = 3.0
    
    for i in range(0, tam):
        p = random.uniform(0, 1)
        if(p < prob):
            sd = ((Ui[i] - Li[i])/10.0)
            g = random.gauss(ind[i], sd)
            ind[i] = g
            if(ind[i] < Li[i]):
                ind[i] = Li[i]
            if(ind[i] > Ui[i]):
                ind[i] = Ui[i]

def mutPerm(ind, prob):

    tam = len(ind)
    
    for i in range(0, tam):    
        p = random.uniform(0, 1)
        if(p < prob):
            a1 = i
            a2 = a1
            while(a2 == a1):
                a2 = random.randrange(0, tam)
            temp = ind[a1]
            ind[a1] = ind[a2]
            ind[a2] = temp
            
def aplicaMutacao(tipo, perm, ind, prob, Li, Ui):

    if(tipo == 'BIN'):
        mutBin(ind, prob)
    elif(tipo == 'INT'):
        if(perm == True):
            mutPerm(ind, prob)
        else:
            mutIntNPerm(ind, prob, Li, Ui)
    else:
        #mutDelta(ind, prob, Li, Ui)
        mutGauss(ind, prob, Li, Ui)

def rotinaMutacao(matriz, tipo, perm, prob, Li, Ui):

    POP = len(matriz)
    mut = copy.deepcopy(matriz)
    
    for i in range(0, POP):
        aplicaMutacao(tipo, perm, mut[i], prob, Li, Ui)
    
    return mut
