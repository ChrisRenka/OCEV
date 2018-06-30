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
import pygame

import leitura
import populacao
import diversidade
import binConv
import selecEscLin
import crossover
import mutacao
import fitAux

matrizLab = []
#matrizDist = []
inicioLab = [-1,-1]
fimLab = [-1,-1]
maiorDist = 0


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

def rotinaEvolucao(arqEnt, arqEvol, arqLab):

    TIPO, POP, D, Li, Ui, extra = leitura.entrada(arqEnt)
    sel, elite, cxTipo, cxProb, mutProb, passos, nExec = leitura.paramEvo(arqEvol)
    
    arqFit = open('fitness.txt', 'w')
    #arqDivPar = open('diversidadePar.txt', 'w')
    #arqDivCentro = open('diversidadeCentro.txt', 'w')
    arqDivDPM = open('diversidadeDPM.txt', 'w')
    arqDPM = open('dpmFitness.txt', 'w')
    
    melhorFitLista = [0.0]*passos
    mediaFitLista = [0.0]*passos
    dpmFitLista = [0.0]*passos
    #divParLista = [0.0]*passos
    #divCentroLista = [0.0]*passos
    divDPMLista = [0.0]*passos
    
    #global matrizLab
    #global inicioLab
    #global fimLab
    #global maiorDist
    
    leituraLab(arqLab)
    
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
    processes = [mp.Process(target=evolui, args=(TIPO, POP, D, copy.deepcopy(Li), copy.deepcopy(Ui), extra, sel, elite, cxTipo, cxProb, mutProb, passos, saida)) for x in range(nExec)]
    
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
            divDPMLista[j] += r[5][j]
    
    
    for i in range(0, passos):
        melhorFitLista[i] = melhorFitLista[i]/nExec
        mediaFitLista[i] = mediaFitLista[i]/nExec
        dpmFitLista[i] = dpmFitLista[i]/nExec
        #print(dpmFitLista[i])
        #divParLista[i] = divParLista[i]/nExec
        #divCentroLista[i] = divCentroLista[i]/nExec
        divDPMLista[i] = divDPMLista[i]/nExec
        
        s = '{} {} {} {} {}\n'.format(i, melhorFitLista[i], mediaFitLista[i], (mediaFitLista[i] + dpmFitLista[i]), (mediaFitLista[i] - dpmFitLista[i]))
        arqFit.write(s)
        
        #s = '{} {}\n'.format(i, divParLista[i])
        #arqDivPar.write(s)
        
        #s = '{} {}\n'.format(i, divCentroLista[i])
        #arqDivCentro.write(s)
        
        s = '{} {}\n'.format(i, divDPMLista[i])
        arqDivDPM.write(s)   

        s = '{} {}\n'.format(i, dpmFitLista[i])
        arqDPM.write(s)
    
    #objetivo = objetivoIndiv(melhorInd) ##### 8 rainhas
    #lucro = lucroIndiv(melhorInd, matrizLucro)
    percurso = marcaIndiv(melhorInd)
    
    return melhorInd, percurso, melhorFit
    
def evolui(TIPO, POP, D, Li, Ui, extra, sel, elite, cxTipo, cxProb, mutProb, passos, saida):
    
    matriz = populacao.geraPop(TIPO, POP, D, Li, Ui, extra)
    fit = fitPop(matriz) ##### 8 rainhas
    max = True  #### minimizar ou maximizar
    
    melhorFitLista = [0.0]*passos
    mediaFitLista = [0.0]*passos
    dpmFitLista = [0.0]*passos
    divDPMLista = [0.0]*passos
    
    i = 0
    maior = fitAux.melhorFitFunc(fit, max)
    media = fitAux.mediaFit(fit)
    dpm = fitAux.desvioPadraoFit(fit, media, POP)
    
    melhorFitLista[i] += maior
    mediaFitLista[i] += media
    dpmFitLista[i] += dpm
	
    
    #divPar = diversidade.diversidadePar(TIPO, matriz, Li, Ui)
    #divCentro = diversidade.diversidadeCentro(TIPO, matriz, Li, Ui)
    divDPM = diversidade.diversidadeDPMedio(TIPO, matriz)
    #s = '{} {} {}\n'.format(i, divPar, divCentro)
    #arqDiv.write(s)
    #divParLista[i] += divPar
    #divCentroLista[i] += divCentro
    divDPMLista[i] += divDPM
    
    melhorFitTotal = maior
    melhorIndTotal = copy.deepcopy(matriz[fitAux.elitismo(fit)])
    
    c = 1.2
    passosCrescer = selecEscLin.cPassosCrescer(passos, 0.2)
    #g = 0.5
    #gapPassos = selecEscLin.genGapPasso(passos)
    g = 1.0
    
    for i in range(1, passos):      
        
        if(elite == True and max == True):
            eliteInd = fitAux.elitismo(fit)
            eliteCod = copy.deepcopy(matriz[eliteInd])
        elif(elite == True and max == False):
            eliteInd = fitAux.elitismoMin(fit)
            eliteCod = copy.deepcopy(matriz[eliteInd])
        
        #####
        #g = selecEscLin.genGapNovo(g, i, passos, gapPassos)
        #if(g>1.0):
        #    print('g maior que 1!')
        
        sl, gap = selecEscLin.selecao(matriz, fit, POP, sel, max, c, g)
        cross = crossover.rotinaCrossOver(sl, TIPO, extra, cxTipo, cxProb, Li, Ui)
        mut = mutacao.rotinaMutacao(cross, TIPO, extra, mutProb, Li, Ui)
        
        c = selecEscLin.aumentaC(c, i, passosCrescer)
        
        if(elite == True):
            sub = random.randrange(0, int(POP*g))
            mut[sub] = eliteCod
        
        matriz = (copy.deepcopy(mut) + gap)
        fit = fitPop(matriz) ##### 8 rainhas
        
        #pool = mp.Pool(processes=2)
        #fit = pool.map(fitIndiv, matriz)
        
        #if(fit != fitTeste):
        #    print('nope')
        
        maior = fitAux.melhorFitFunc(fit, max)
        media = fitAux.mediaFit(fit)
        dpm = fitAux.desvioPadraoFit(fit, media, POP)
        #s = '{} {} {}\n'.format(i, maior, media)
        #arqFit.write(s)
        melhorFitLista[i] += maior
        mediaFitLista[i] += media
        dpmFitLista[i] += dpm
        
        #divPar = diversidade.diversidadePar(TIPO, matriz, Li, Ui)
        #divCentro = diversidade.diversidadeCentro(TIPO, matriz, Li, Ui)
        divDPM = diversidade.diversidadeDPMedio(TIPO, matriz)
        #s = '{} {} {}\n'.format(i, divPar, divCentro)
        #arqDiv.write(s)
        #divParLista[i] += divPar
        #divCentroLista[i] += divCentro
        divDPMLista[i] += divDPM
        
        if(max == True and maior > melhorFitTotal):
            melhorIndTotal = copy.deepcopy(matriz[fitAux.elitismo(fit)])
            melhorFitTotal = maior
        elif(max == False and maior < melhorFitTotal):
            melhorIndTotal = copy.deepcopy(matriz[fitAux.elitismoMin(fit)])
            melhorFitTotal = maior
    
    #melhorInt, result = pesResultadoIndiv(melhorIndTotal, D, Li, Ui, extra)   ###### função da fábrica de rádios
    
    saida.put([melhorIndTotal, melhorFitTotal, melhorFitLista, mediaFitLista, dpmFitLista, divDPMLista])
    
########

def leituraLab(arq):

    arquivo = open(arq, 'r')
    global matrizLab
    global inicioLab
    global fimLab
    global maiorDist
    
    matrizLab = arquivo.read().splitlines()
    linhas = len(matrizLab)
    colunas = len(matrizLab[0])
    
    maiorDist = linhas + colunas - 2 #maior distância no tabuleiro
    
    cont = 0
    for i in range(0, linhas):
        for j in range(0, colunas):
            if(matrizLab[i][j] == '1'):
                inicioLab = [i, j]
                cont += 1
                if(cont == 2):
                    break;
            elif(matrizLab[i][j] == '2'):
                fimLab = [i, j]
                cont += 1
                if(cont == 2):
                    break;
        if(cont == 2):
            break

def vizinhos(pos):

    viz = []
    if(matrizLab[pos[0]-1][pos[1]] != '9'):
        viz.append([pos[0]-1, pos[1]])
    if(matrizLab[pos[0]][pos[1]+1] != '9'):
        viz.append([pos[0], pos[1]+1])
    if(matrizLab[pos[0]+1][pos[1]] != '9'):
        viz.append([pos[0]+1, pos[1]])
    if(matrizLab[pos[0]][pos[1]-1] != '9'):
        viz.append([pos[0], pos[1]-1])
    
    return viz
    
def proxPos(posAtual, vInd):

    viz = vizinhos(posAtual)
    nViz = len(viz)
    
    return viz[vInd//(12//nViz)]
    
    '''
    if(nViz == 1):
        prox = copy.deepcopy(viz[0])
    elif(nViz == 2):
        if(vInd < 6):
            prox = copy.deepcopy(viz[0])
        else:
            prox = copy.deepcopy(viz[1])
    elif(nViz == 3):
        if(vInd < 4):
            prox = copy.deepcopy(viz[0])
        elif(vInd < 8):
            prox = copy.deepcopy(viz[1])
        else:
            prox = copy.deepcopy(viz[2])
    else:
        if(vInd < 3):
            prox = copy.deepcopy(viz[0])
        elif(vInd < 6):
            prox = copy.deepcopy(viz[1])
        elif(vInd < 9):
            prox = copy.deepcopy(viz[2])
        else:
            prox = copy.deepcopy(viz[3])
    
    return prox
    '''
        
def fitIndiv(indiv):
    
    atual = copy.deepcopy(inicioLab)
    
    for i in indiv:
        atual = proxPos(atual, i)
        if(matrizLab[atual[0]][atual[1]] == '2'):
            return 1.0
    
    dist = abs(atual[0] - fimLab[0]) + abs(atual[1] - fimLab[1])
    return ((maiorDist - dist)/maiorDist)

def fitPop(matriz):
    
    fit = []
    for i in matriz:
        fit.append(fitIndiv(i))
    
    return fit

def marcaIndiv(indiv):

    matrizPercurso = copy.deepcopy(matrizLab)
    for i in range(0, len(matrizPercurso)):
        matrizPercurso[i] = list(matrizPercurso[i])
    
    atual = copy.deepcopy(inicioLab)
    
    for i in indiv:
        atual = proxPos(atual, i)
        if(matrizLab[atual[0]][atual[1]] == '2'):
            return matrizPercurso
        elif(matrizLab[atual[0]][atual[1]] != '1'):
            matrizPercurso[atual[0]][atual[1]] = '3'
    
    matrizPercurso[atual[0]][atual[1]] = '4'
    
    return matrizPercurso
            
'''
def calculaDist():

    global matrizDist
    global maiorDist
    fimX = fimLab[0]
    fimY = fimLab[1]
    linhas = len(matrizLab)
    colunas = len(matrizLab[0])
    
    for i in range(0, linhas):
        matrizDist.append([-1]*colunas)
    
    matrizDist[fimX][fimY] = 0
    
    fila = []
    fila.append([fimX, fimY])
    
    while(len(fila) > 0):
        atual = fila.pop(0)
        ax = atual[0]
        ay = atual[1]
        
        buscaViz(ax, ay, 1, 0, fila, linhas, colunas)
        buscaViz(ax, ay, 0, 1, fila, linhas, colunas)
        buscaViz(ax, ay, -1, 0, fila, linhas, colunas)
        buscaViz(ax, ay, 0, -1, fila, linhas, colunas)
    
    maiorDist = matrizDist[ax][ay]
            

def buscaViz(ax, ay, dx, dy, fila, mx, my):
    
    global matrizDist
    
    if( (ax+dx > (mx-1)) or (ay+dy > (my-1)) ):
        return
    
    if(matrizLab[ax+dx][ay+dy] != '9'):
        if( (matrizDist[ax+dx][ay+dy] == -1) or (matrizDist[ax+dx][ay+dy] > (matrizDist[ax][ay] + 1)) ):
            matrizDist[ax+dx][ay+dy] = matrizDist[ax][ay] + 1
            fila.append([ax+dx, ay+dy])
'''
########

######## pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLUE =  (0, 0, 255) 
MARRON = (92,64,51) 
GREEN = (0, 255, 0) 
RED =   (255, 0, 0) 
YELLOW = (255, 255, 51)

ORANGE = (255, 128, 0)

def mostraResultado(percurso):

    pygame.init()

    #definindo tela 840x840
    screen = pygame.display.set_mode((len(percurso[0])*20, len(percurso)*20))
    # carregando fonte
    font = pygame.font.SysFont(None, 55)

    pygame.display.set_caption('Percurso')

    # preenchendo o fundo com preto
    screen.fill(BLACK)

    mostraCampo(screen, percurso)
    #posicoes(matriz, inicio, fim)

    espera()

def mostraCampo(screen, pecurso):
    
    linhas = len(percurso)
    colunas = len(percurso[0])
    
    for i in range(0, linhas):
        for j in range(0, colunas):
            if(percurso[i][j] == '9'):
                pygame.draw.rect(screen, BLACK, [j*20, i*20, 20, 20])
            elif(percurso[i][j] == '0'):
                pygame.draw.rect(screen, WHITE, [j*20, i*20, 20, 20])
            elif(percurso[i][j] == '3'):
                pygame.draw.rect(screen, YELLOW, [j*20, i*20, 20, 20])
            elif(percurso[i][j] == '1'):
                pygame.draw.rect(screen, GREEN, [j*20, i*20, 20, 20])
            elif(percurso[i][j] == '2'):
                pygame.draw.rect(screen, RED, [j*20, i*20, 20, 20])
            else:
                pygame.draw.rect(screen, ORANGE, [j*20, i*20, 20, 20])
            
    
    pygame.display.flip()
    
    return

def espera():
    while True:
        # capturando eventos
        event = pygame.event.poll()
        # caso o evento QUIT (clicar no x da janela) seja disparado
        if event.type == pygame.QUIT:
            # saia do loop finalizando o programa
            break

########


random.seed(time.time())

arqEnt = 'paramPop.txt'
arqEvol = 'paramEvol.txt'
arqLab = 'labirinto.txt'


inicio = time.time()
melhorInd, percurso, melhorFit = rotinaEvolucao(arqEnt, arqEvol, arqLab)
#restricoes = avaliaRestricoes(melhorInd)
fim = time.time()

print("Melhor indivíduo:")
print(melhorInd)
print()
#print("Quantidade de colisões do indivíduo:")
#print(result)
#print()
#print("Lucro do indivíduo:")
#print(lucro)
print("Fitness do melhor indivíduo:")
print(melhorFit)
print()
print("Tempo de execução:")
print("{} s".format(fim-inicio))

mostraResultado(percurso)


#arqLab = 'labirinto.txt'
#leituraLab(arqLab)
#print(vizinhos([8, 6]))







