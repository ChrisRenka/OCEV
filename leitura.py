import sys

def entrada(arq):
    
    arquivo = open(arq, 'r')
    linhas = arquivo.read().splitlines()
    linhas.append("0 0")
    
    t, TIPO = linhas[0].split(" ")
    pop, POP = linhas[1].split(" ")
    POP = int(POP)
    d, D = linhas[2].split(" ")
    D = int(D)
    if(TIPO == 'BIN'):
        if(len(linhas)>=6):
            l5 = linhas[5].split(" ")
            if(l5[1] == 'REAL' or l5[1] == 'INT'):
                li = linhas[3].split(" ")
                ui = linhas[4].split(" ")
                Li = []
                Ui = []
                if(D > 1):  # gera as listas de Li e Ui
                    if(len(li) == 2):
                        for i in range(0, D):
                            Li.append(float(li[1]))
                    elif(len(li) == (D+1)):
                        for i in range(0, D):
                            Li.append(float(li[i+1]))
                    else:
                        print("Quantidade incorreta de limites inferiores em entrada.txt")
                        sys.exit()
                    
                    if(len(ui) == 2):
                        for i in range(0, D):
                            Ui.append(float(ui[1]))
                    elif(len(ui) == (D+1)):
                        for i in range(0, D):
                            Ui.append(float(ui[i+1]))
                    else:
                        print("Quantidade incorreta de limites superiores em entrada.txt")
                        sys.exit()
                
                if(len(l5) == 3):
                    cod, COD, dec = linhas[5].split(" ")
                    dec = int(dec)
                    return TIPO, POP, D, Li, Ui, (COD, dec)
                cod, COD = linhas[5].split(" ")
                return TIPO, POP, D, Li, Ui, COD
        
        return TIPO, POP, D, 0, 0, False
    
    if(TIPO == 'REAL'):
        li = linhas[3].split(" ")
        ui = linhas[4].split(" ")
        Li = []
        Ui = []
        if(D > 1):  # gera as listas de Li e Ui
            if(len(li) == 2):
                for i in range(0, D):
                    Li.append(float(li[1]))
            elif(len(li) == (D+1)):
                for i in range(0, D):
                    Li.append(float(li[i+1]))
            else:
                print("Quantidade incorreta de limites inferiores em entrada.txt")
                sys.exit()
            
            if(len(ui) == 2):
                for i in range(0, D):
                    Ui.append(float(ui[1]))
            elif(len(ui) == (D+1)):
                for i in range(0, D):
                    Ui.append(float(ui[i+1]))
            else:
                print("Quantidade incorreta de limites superiores em entrada.txt")
                sys.exit()
        
        return TIPO, POP, D, Li, Ui, False
    
    else:
        if(d == 'Li:'):
            Li = D
            ui, Ui = linhas[3].split(" ")
            Ui = int(Ui)
            D = Ui - Li + 1
            return TIPO, POP, D, [Li]*D, [Ui]*D, True
        
        prox = linhas[3].split(" ")
        if(prox[0] == 'Li:'):
            #Li = int(PROX)
            ui = linhas[4].split(" ")
            #Ui = int(Ui)
            perm, PERM = linhas[5].split(" ")
            PERM = bool(int(PERM))
            if(PERM == True):
                return TIPO, POP, D, [int(prox[1])]*D, [int(ui[1])]*D, True
            Li = []
            Ui = []
            if(D > 1):  # gera as listas de Li e Ui
                if(len(prox) == 2):
                    for i in range(0, D):
                        Li.append(int(prox[1]))
                elif(len(prox) == (D+1)):
                    for i in range(0, D):
                        Li.append(int(prox[i+1]))
                else:
                    print("Quantidade incorreta de limites inferiores em entrada.txt")
                    sys.exit()
                
                if(len(ui) == 2):
                    for i in range(0, D):
                        Ui.append(int(ui[1]))
                elif(len(ui) == (D+1)):
                    for i in range(0, D):
                        Ui.append(int(ui[i+1]))
                else:
                    print("Quantidade incorreta de limites superiores em entrada.txt")
                    sys.exit()
            
            return TIPO, POP, D, Li, Ui, False
        return TIPO, POP, D, [0]*D, [D-1]*D, True

def paramEvo(arq):

    arquivo = open(arq, 'r')
    linhas = arquivo.read().splitlines()
    
    sel = linhas[0].split(" ")
    elite = linhas[1].split(" ")
    cxTipo = linhas[2].split(" ")
    cxProb = linhas[3].split(" ")
    mutProb = linhas[4].split(" ")
    passos = linhas[5].split(" ")
    nExec = linhas[6].split(" ")
    
    return int(sel[1]), bool(int(elite[1])), int(cxTipo[1]), float(cxProb[1]), float(mutProb[1]), int(passos[1]), int(nExec[1])