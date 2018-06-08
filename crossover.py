import random
import copy

def cxUmPonto(ind1, ind2):

    tam = len(ind1)
    novo1 = []
    novo2 = []
    
    ponto = random.randrange(1, tam)
    #print(ponto)
    
    for i in range(0, ponto):
        novo1.append(ind1[i])
        novo2.append(ind2[i])
    for i in range(ponto, tam):
        novo1.append(ind2[i])
        novo2.append(ind1[i])
    
    return novo1, novo2

def cxDoisPontos(ind1, ind2):

    tam = len(ind1)
    novo1 = []
    novo2 = []
    
    ponto1 = random.randrange(1, tam)
    ponto2 = ponto1
    while(ponto2 == ponto1):
        ponto2 = random.randrange(1, tam)
    #print(ponto1)
    #print(ponto2)
    
    if(ponto1>ponto2):
        temp = ponto1
        ponto1 = ponto2
        ponto2 = temp
    
    cortes = random.uniform(0,1)
    if(cortes < 0.5):
        for i in range(0, ponto1):
            novo1.append(ind1[i])
            novo2.append(ind2[i])
        for i in range(ponto1, ponto2):
            novo1.append(ind2[i])
            novo2.append(ind1[i])
        for i in range(ponto2, tam):
            novo1.append(ind1[i])
            novo2.append(ind2[i])
    else:
        for i in range(0, ponto1):
            novo1.append(ind2[i])
            novo2.append(ind1[i])
        for i in range(ponto1, ponto2):
            novo1.append(ind1[i])
            novo2.append(ind2[i])
        for i in range(ponto2, tam):
            novo1.append(ind2[i])
            novo2.append(ind1[i])
        
    return novo1, novo2
    
def cxUniforme(ind1, ind2):

    tam = len(ind1)
    novo1 = []
    novo2 = []
    
    for i in range(0, tam):
        prob = random.uniform(0, 1)
        if(prob < 0.5):
            novo1.append(ind1[i])
            novo2.append(ind2[i])
        else:
            novo1.append(ind2[i])
            novo2.append(ind1[i])
    
    return novo1, novo2
    
def cxBinInt(ind1, ind2, cxTipo):

    if(cxTipo == 1):
        novo1, novo2 = cxUmPonto(ind1, ind2)
    elif(cxTipo == 2):
        novo1, novo2 = cxDoisPontos(ind1, ind2)
    else:
        novo1, novo2 = cxUniforme(ind1, ind2)
    
    return novo1, novo2

def cxBLX(ind1, ind2, Li, Ui):

    a = 0.5
    tam = len(ind1)
    novo1 = []
    novo2 = []
    
    for i in range(0, tam):
        d = abs(ind1[i] - ind2[i])
        
        r = random.uniform((min(ind1[i], ind2[i]) - a*d), (max(ind1[i], ind2[i]) + a*d))
        novo1.append(r)
        if( (novo1[i] < Li[i]) or (novo1[i] > Ui[i]) ):
            if(novo1[i] < Li[i]):
                novo1[i] = Li[i]
            elif(novo1[i] > Ui[i]):
                novo1[i] = Ui[i]
        
        r = random.uniform((min(ind1[i], ind2[i]) - a*d), (max(ind1[i], ind2[i]) + a*d))
        novo2.append(r)
        if( (novo2[i] < Li[i]) or (novo2[i] > Ui[i]) ):
            if(novo2[i] < Li[i]):
                novo2[i] = Li[i]
            elif(novo2[i] > Ui[i]):
                novo2[i] = Ui[i]
    
    return novo1, novo2

def cxUniformAverage(ind1, ind2):

    tam = len(ind1)
    novo1 = []
    novo2 = []
    
    for i in range(0, tam):
        m = (ind1[i] + ind2[i])/2.0
        prob = random.uniform(0, 1)
        if(prob < 0.5):
            novo1.append(m)
            novo2.append(ind2[i])
        else:
            novo1.append(ind1[i])
            novo2.append(m)
    
    return novo1, novo2

def cxAri(ind1, ind2, Li, Ui):

    tam = len(ind1)
    novo1 = []
    novo2 = []
    
    a = random.uniform(0,1)
    for i in range(0, tam):
        novo1.append(a*ind1[i] + (1-a)*ind2[i])
        if( (novo1[i] < Li[i]) or (novo1[i] > Ui[i]) ):
            if(novo1[i] < Li[i]):
                novo1[i] = Li[i]
            elif(novo1[i] > Ui[i]):
                novo1[i] = Ui[i]
        
        novo2.append((1-a)*ind1[i] + a*ind2[i])
        if( (novo2[i] < Li[i]) or (novo2[i] > Ui[i]) ):
            if(novo2[i] < Li[i]):
                novo2[i] = Li[i]
            elif(novo2[i] > Ui[i]):
                novo2[i] = Ui[i]
    
    return novo1, novo2

def cxReal(ind1, ind2, cxTipo, Li, Ui):

    if(cxTipo == 1):
        novo1, novo2 = cxBLX(ind1, ind2, Li, Ui)
    elif(cxTipo == 2):
        novo1, novo2 = cxUniformAverage(ind1, ind2)
    else:
        novo1, novo2 = cxAri(ind1, ind2, Li, Ui)
    
    return novo1, novo2

def cxPMX(ind1, ind2, Li):

    tam = len(ind1)
    novo1 = [Li-1]*tam
    novo2 = [Li-1]*tam
    
    ponto1 = random.randrange(1, tam)
    ponto2 = ponto1
    while(ponto2 == ponto1):
        ponto2 = random.randrange(1, tam)
    
    if(ponto1>ponto2):
        temp = ponto1
        ponto1 = ponto2
        ponto2 = temp
    #print(ponto1)
    #print(ponto2)
        
    for i in range(ponto1, ponto2):
        novo1[i] = ind2[i]
        novo2[i] = ind1[i]
    
    for i in range(0, ponto1):
        idx = i
        while(True):
            try:
                idx = novo1.index(ind1[idx], ponto1, ponto2)
                #novo1[i] = ind1[idx]
            except ValueError:
                novo1[i] = ind1[idx]
                break
        
        idx = i
        while(True):
            try:
                idx = novo2.index(ind2[idx], ponto1, ponto2)
                #novo2[i] = ind2[idx]
            except ValueError:
                novo2[i] = ind2[idx]
                break
    
    for i in range(ponto2, tam):
        idx = i
        while(True):
            try:
                idx = novo1.index(ind1[idx], ponto1, ponto2)
                #novo1[i] = ind1[idx]
            except ValueError:
                novo1[i] = ind1[idx]
                break
        
        idx = i
        while(True):
            try:
                idx = novo2.index(ind2[idx], ponto1, ponto2)
                #novo2[i] = ind2[idx]
            except ValueError:
                novo2[i] = ind2[idx]
                break
    
    return novo1, novo2
    
def aplicaCrossOver(tipo, perm, ind1, ind2, cxTipo, Li, Ui):

    if(tipo == 'BIN'):
        novo1, novo2 = cxBinInt(ind1, ind2, cxTipo)
    elif(tipo == 'INT'):
        if(perm == True):
            novo1, novo2 = cxPMX(ind1, ind2, Li[0])
        else:
            novo1, novo2 = cxBinInt(ind1, ind2, cxTipo)
    else:
        novo1, novo2 = cxReal(ind1, ind2, cxTipo, Li, Ui)
    
    return novo1, novo2

def rotinaCrossOver(matriz, tipo, perm, cxTipo, cxProb, Li, Ui):

    POP = len(matriz)
    nova = []
    
    ind1 = []
    ind2 = []
    for i in range(0, POP):
        prob = random.uniform(0, 1)
        if(prob > cxProb):
            nova.append(matriz[i])
        else:
            if(ind1 == []):
                ind1 = copy.deepcopy(matriz[i])
            else:
                ind2 = copy.deepcopy(matriz[i])
                novo1, novo2 = aplicaCrossOver(tipo, perm, ind1, ind2, cxTipo, Li, Ui)
                nova.append(novo1)
                nova.append(novo2)
                ind1 = []
                ind2 = []
    if(ind1 != [] and ind2 == []):
        nova.append(ind1)
    
    return nova