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
import multiprocessing as mp

import leitura
#import populacao
#import diversidade
#import binConv
#import selecEscLin
#import crossover
#import mutacao
import fitAux

matrizLucro = []
maiorLucro = 0
totalCol = 0


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
    
    arqFit = open('rsFitness.txt', 'w')
    #arqDivPar = open('diversidadePar.txt', 'w')
    #arqDivCentro = open('diversidadeCentro.txt', 'w')
    #arqDivDPM = open('diversidadeDPM.txt', 'w')
    arqDPM = open('rsDpmFitness.txt', 'w')
    
    melhorFitLista = [0.0]*passos
    mediaFitLista = [0.0]*passos
    dpmFitLista = [0.0]*passos
    #divParLista = [0.0]*passos
    #divCentroLista = [0.0]*passos
    #divDPMLista = [0.0]*passos
    
    global matrizLucro
    global maiorLucro
    global totalCol
	
    matrizLucro, maiorLucro = geraMatrizLucro(D)
    totalCol = totalPares(D)
    
    max = True
    if(max == True):
        melhorFit = -100.0
    else:
        melhorFit = 9000000.0
    melhorInd = []
    
    saida = mp.Queue()
    
    '''
    for i in range(0, nExec):
        melhorIndAtual, melhorFitAtual = evolui(TIPO, POP, D, Li, Ui, extra, sel, elite, cxTipo, cxProb, mutProb, passos, melhorFitLista, mediaFitLista, divDPMLista)
        if(max == True and melhorFitAtual > melhorFit):
            melhorFit = melhorFitAtual
            melhorInd = copy.deepcopy(melhorIndAtual)
        elif(max == False and melhorFitAtual < melhorFit):
            melhorFit = melhorFitAtual
            melhorInd = copy.deepcopy(melhorIndAtual)
    '''
    processes = [mp.Process(target=evolui, args=(TIPO, POP, D, copy.deepcopy(Li), copy.deepcopy(Ui), passos, saida)) for x in range(nExec)]
    
    for p in processes:
        p.start()
    
    #for p in processes:
    #    p.join()
    resultados = []
    while 1:
        running = any(p.is_alive() for p in processes)
        while not saida.empty():
           #process_queue_data()
           resultados.append(saida.get())
        if not running:
            break
        time.sleep(0.5)
    
    #resultados = [saida.get() for p in processes]
    #for i in resultados:
    #    print(i)
    
    if(max == True):    
        for i in resultados:
            if(i[1] > melhorFit):
                melhorFit = i[1]
                melhorInd = copy.deepcopy(i[0])
    else:
        for i in resultados:
            if(i[1] < melhorFit):
                melhorFit = i[1]
                melhorInd = copy.deepcopy(i[0])
    
    for r in resultados:
        for j in range(0, passos):
            melhorFitLista[j] += r[2][j]
            mediaFitLista[j] += r[3][j]
            dpmFitLista[j] += r[4][j]
    
    
    for i in range(0, passos):
        melhorFitLista[i] = melhorFitLista[i]/nExec
        mediaFitLista[i] = mediaFitLista[i]/nExec
        dpmFitLista[i] = dpmFitLista[i]/nExec
        #print(dpmFitLista[i])
        #divParLista[i] = divParLista[i]/nExec
        #divCentroLista[i] = divCentroLista[i]/nExec
        #divDPMLista[i] = divDPMLista[i]/nExec
        
        s = '{} {} {} {} {}\n'.format(i, melhorFitLista[i], mediaFitLista[i], (mediaFitLista[i] + dpmFitLista[i]), (mediaFitLista[i] - dpmFitLista[i]))
        arqFit.write(s)
        
        #s = '{} {}\n'.format(i, divParLista[i])
        #arqDivPar.write(s)
        
        #s = '{} {}\n'.format(i, divCentroLista[i])
        #arqDivCentro.write(s)
        
        #s = '{} {}\n'.format(i, divDPMLista[i])
        #arqDivDPM.write(s)   

        s = '{} {}\n'.format(i, dpmFitLista[i])
        arqDPM.write(s)
    
    objetivo = objetivoIndiv(melhorInd) ##### 8 rainhas
    lucro = lucroIndiv(melhorInd, matrizLucro)
    
    return melhorInd, objetivo, lucro, melhorFit
    
def evolui(TIPO, POP, D, Li, Ui, passos, saida):
    
    totalPassos = passos*POP
    ger = 0
    Li = Li[0]
    Ui = Ui[0]
    
    melhorFitLista = [0.0]*passos
    mediaFitLista = [0.0]*passos
    dpmFitLista = [0.0]*passos
    
    fitTemp = [0.0]*POP
    temp = 1
    
    melhorIndiv = random.sample(range(Li, Ui+1), Ui - Li + 1)
    melhorFit = fitIndiv(melhorIndiv)
    fitTemp[0] = melhorFit
    
    fitMedioPop = melhorFit
    for i in range(1, totalPassos):
        indivAtual = random.sample(range(Li, Ui+1), Ui - Li + 1)
        fitAtual = fitIndiv(indivAtual)
        fitMedioPop += fitAtual
        fitTemp[temp] = fitAtual
        temp += 1
        
        if(fitAtual > melhorFit):
            melhorIndiv = copy.deepcopy(indivAtual)
            melhorFit = fitAtual
        
        if(i == (ger*POP + (POP - 1))):
            fitMedioPop = fitMedioPop/POP
            dpm = fitAux.desvioPadraoFit(fitTemp, fitMedioPop, POP)
            
            melhorFitLista[ger] += melhorFit
            mediaFitLista[ger] += fitMedioPop
            dpmFitLista[ger] += dpm
            
            fitMedioPop = 0.0
            temp = 0
            ger += 1
            
    
    saida.put([melhorIndiv, melhorFit, melhorFitLista, mediaFitLista, dpmFitLista])
    
########

def totalPares(tam):

    return (math.factorial(tam)/(2*math.factorial(tam-2)))

def objetivoIndiv(indiv):

    tam = len(indiv)
    
    fo = 0
    for i in range(0, tam):
        for j in range(i+1, tam):
            hor = abs(i - j)
            ver = abs(indiv[i] - indiv[j])
            if(hor == ver):
                fo += 1
        
    return fo

def fitPop(matriz):

    POP = len(matriz)
    tam = len(matriz[0])    
    total = totalPares(tam)
    
    fit = []
    for i in range(0, POP):
        colInd = (objetivoIndiv(matriz[i]))/total
        lucroInd = lucroIndivNorm(matriz[i], matrizLucro, maiorLucro)
        fitInd = (lucroInd - colInd)
        fit.append(fitInd)
    
    return fit

def fitIndiv(indiv):

    fit = 0
    colInd = (objetivoIndiv(indiv))/totalCol
    lucroInd = lucroIndivNorm(indiv, matrizLucro, maiorLucro)
    fit = (lucroInd - colInd)
    
    return fit

def lucroIndiv(indiv, matriz):

    lucro = 0
    tam = len(indiv)
    
    for i in range(0, tam):
        lucro += matriz[i][indiv[i]]
    
    return lucro

def lucroIndivNorm(indiv, matriz, lucroMax):

    lucro = lucroIndiv(indiv, matriz)
    
    return (lucro/lucroMax)
    
def geraMatrizLucro(tam):
    
    valor = 1
    maiorLucro = 0
    mat = []
    for i in range(0, tam):
        linha = []
        for j in range(0, tam):
            if((i+1)%2 == 1):
                linha.append(math.sqrt(valor))
            else:
                linha.append(math.log10(valor))
            valor += 1
        mat.append(linha)
    
    for j in range(0, tam):
        maiorLucro += mat[tam-2][j]
    
    return mat, maiorLucro

def printMat(mat):
    
    for i in mat:
        print(i)
        print()

def printIndivLucro(indiv, matriz):

    tam = len(indiv)
    for i in range(0, tam):
        print(matriz[i][indiv[i]])
        print()
   
########


random.seed(time.time())

arqEnt = 'paramPop.txt'
arqEvol = 'paramEvol.txt'

inicio = time.time()
melhorInd, result, lucro, melhorFit = rotinaEvolucao(arqEnt, arqEvol)
#restricoes = avaliaRestricoes(melhorInd)
fim = time.time()

print("Melhor indivíduo:")
print(melhorInd)
print()
print("Quantidade de colisões do indivíduo:")
print(result)
print()
print("Lucro do indivíduo:")
print(lucro)
print("Fitness do melhor indivíduo:")
print(melhorFit)
print("Tempo de execução:")
print("{} s".format(fim-inicio))



#mat, maior = geraMatrizLucro(32)
#printMat(mat)
#print(maior)

#fitTeste = [8,5,3,1]
#c = 1.2

#fitEsc = selecEscLin.escalonaFit(fitTeste, c)
#print(fitEsc)

#teste1 = [3,6,2,7,1,0,4,5]
#teste2 = [6, 2, 7, 1, 4, 0, 5, 3]
#printIndivLucro(teste2, mat)
#print(objetivoIndiv(teste))
#print(lucroIndiv(teste, mat))

#teste = [31, 17, 24, 7, 29, 8, 30, 12, 16, 3, 11, 6, 22, 2, 23, 14, 28, 10, 25, 4, 20, 27, 19, 5, 15, 13, 9, 0, 18, 21, 26, 1]
#fit = fitPop([teste], mat, maior)
#print(fit)








