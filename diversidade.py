import math

######## Diversidade calculada pelo método do centro de massa

def diversidadeCentro(tipo, matriz, Li, Ui):
    
    if(len(matriz) == 1):
        return 0
    
    if(tipo == 'BIN'):
        I = diversidadeCentroBin(matriz)
    elif(tipo == 'INT'):
        I = diversidadeCentroInt(matriz, Li, Ui)
    else:
        I = diversidadeCentroReal(matriz, Li, Ui)
    
    return I
    
def diversidadeCentroBin(matriz):
    
    POP = len(matriz)
    D = len(matriz[0])
    
    c = []
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + int(matriz[j][i])
        temp = temp/POP
        c.append(temp)
    
    I = 0
    for i in range(0, D):
        for j in range(0, POP):
            I = I + ((int(matriz[j][i]) - c[i])**2)
    
    return I

def diversidadeCentroInt(matriz, Li, Ui):
    
    POP = len(matriz)
    D = len(matriz[0])
    
    c = []
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + matriz[j][i]
        temp = temp/POP
        c.append(temp)
       
    
    #maxI = 0.0
    #for i in range(0, D):
    #    maxI = maxI + (Ui - Li)**2
    #maxI = math.sqrt(maxDist)
    
    I = 0
    '''
    for i in range(0, D):
        for j in range(0, POP):
            I = I + ((matriz[j][i] - c[i])**2)
    '''
    for i in range(0, POP):
        dist = 0
        for j in range(0, D):
            dist = dist + (matriz[i][j] - c[j])**2
        I = I + dist       # I = I + (math.sqrt(dist))**2
    
    return I
    
def diversidadeCentroReal(matriz, Li, Ui):
    
    POP = len(matriz)
    D = len(matriz[0])
    
    c = []
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + matriz[j][i]
        temp = temp/POP
        c.append(temp)
    
    #maxI = 0.0
    #for i in range(0, D):
    #    maxI = maxI + (Ui - Li)**2
    #maxI = math.sqrt(maxDist)
    
    I = 0
    '''
    for i in range(0, D):
        for j in range(0, POP):
            I = I + ((matriz[j][i] - c[i])**2)
    '''
    for i in range(0, POP):
        dist = 0
        for j in range(0, D):
            dist = dist + (matriz[i][j] - c[j])**2
        I = I + dist       # I = I + (math.sqrt(dist))**2
    
    return math.sqrt(I)

########

######## Diversidade do Renan

def diversidadeDPMedio(tipo, matriz):

    if(len(matriz) == 1):
        return 0
    
    if(tipo == 'BIN'):
        I = diversidadeDPMedioBin(matriz)
    else:
        I = diversidadeDPMedioIntReal(matriz)
    
    return I

def diversidadeDPMedioBin(matriz):

    POP = len(matriz)
    D = len(matriz[0])
    
    c = []
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + int(matriz[j][i])
        temp = temp/POP
        c.append(temp)
        
    I = 0
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + ((int(matriz[j][i]) - c[i])**2)
        temp = temp/(POP - 1)
        temp = math.sqrt(temp)
        I += temp
    I = I/D
    
    return I

def diversidadeDPMedioIntReal(matriz):

    POP = len(matriz)
    D = len(matriz[0])
    
    c = []
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + matriz[j][i]
        temp = temp/POP
        c.append(temp)
        
    I = 0
    for i in range(0, D):
        temp = 0
        for j in range(0, POP):
            temp = temp + ((matriz[j][i] - c[i])**2)
        temp = temp/(POP - 1)
        temp = math.sqrt(temp)
        I += temp
    I = I/D
    
    return I

########

######## Diversidade calculada pela distância entre pares:

def diversidadePar(tipo, matriz, Li, Ui):
    
    if(len(matriz) == 1):
        return 0
    
    if(tipo == 'BIN'):
        div = diversidadeParBin(matriz)
    elif(tipo == 'INT'):
        div = diversidadeParInt(matriz, Li, Ui)
    else:
        div = diversidadeParReal(matriz, Li, Ui)
    
    return div

def diversidadeParBin(matriz):

    POP = len(matriz)
    D = len(matriz[0])
    maxDist = D
    
    #distância de Hamming
    H = 0
    cont = 0
    for j in range(0, POP-1):
        for j2 in range(j+1, POP):
            for i in range(0, D):
                H = H + abs(int(matriz[j][i]) - int(matriz[j2][i]))
            cont = cont + 1
    
    return H/(maxDist*cont)

def diversidadeParInt(matriz, Li, Ui):
    
    POP = len(matriz)
    D = len(matriz[0])
    
    maxDist = 0
    for i in range(0, D):
        maxDist = maxDist + abs(Ui[i] - Li[i])
    
    #distância de Manhattan
    M = 0
    cont = 0
    for j in range(0, POP-1):
        for j2 in range(j+1, POP):
            for i in range(0, D):
                M = M + abs(matriz[j][i] - matriz[j2][i])
            cont = cont + 1
    
    return M/(maxDist*cont)

def diversidadeParReal(matriz, Li, Ui):

    POP = len(matriz)
    D = len(matriz[0])
    
    maxDist = 0.0
    for i in range(0, D):
        maxDist = maxDist + (Ui[i] - Li[i])**2
    maxDist = math.sqrt(maxDist)
    
    #distância euclidiana
    E = 0
    cont = 0
    for j in range(0, POP-1):
        for j2 in range(j+1, POP):
            dist = 0
            for i in range(0, D):
                dist = dist + ((matriz[j][i] - matriz[j2][i])**2)
            dist = math.sqrt(dist)
            cont = cont + 1
            E = E + dist
    
    return E/(maxDist*cont)
