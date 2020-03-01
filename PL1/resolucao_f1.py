#f1 AED

from time import perf_counter_ns
from math import floor
from random import randint

def geraMatriz(l, u):
    m = []
    width = randint(l, u)
    height = randint(l, u)

    for i in range(0, height):
        linha = []
        for j in range(0, width):
            linha.append(randint(0, 20))
        m.append(linha)
    return m

def Swap(m, head_xy, tail_xy, dq):
    """
    Esta função manipula as coordenadas
    dos elementos dos quadrantes e só depois
    é que faz a troca dos mesmos.
    O ponteiro tail é calculado com base
    no head e na dimensao dos quadrantes.
    Quando head está no 1o ou no 3o quadrante,
    tail está no 4o ou 2o, respetivamente.
    Quando head não se encontra em nenhum dos dois
    quadrantes acima, devolve a sua posicao atual.
    head_xy -> começa em [0, 0]
    tail_xy -> começa em [len(matriz) - (dq[0] - 1), len(matriz[0]) - (dq[1] - 1)]
    dq -> dimensoes quadrante
    """
    
    tail_xy[1] = head_xy[1] + dq[1]

    if (len(m[0]) % 2 == 1):
    #se tiver colunas impares
        tail_xy[1] += 1 
    
    #head esta no 1o quadrante
    if(head_xy[0] in range(dq[0])):
        tail_xy[0] = head_xy[0] + dq[0]
        if (len(m) % 2 == 1):
            tail_xy[0] += 1  #se tiver linhas impares
    elif(head_xy[0] in range(len(m) - dq[0], len(m))):
        tail_xy[0] = head_xy[0] - dq[0]
        if (len(m) % 2 == 1):
            tail_xy[0] -= 1 #se tiver linhas impares
    else: return head_xy

    #troca dos elementos
    m[int(head_xy[0])][int(head_xy[1])], m[int(tail_xy[0])][int(tail_xy[1])] = m[int(tail_xy[0])][int(tail_xy[1])], m[int(head_xy[0])][int(head_xy[1])]
    return head_xy

def trocaQuadrantes(m):
    #calcular a dimensao de cada quadrante
    dq = [floor(len(m)/2), floor(len(m[0])/2)]

    tail_xy = [len(m) - (dq[0] - 1), len(m[0]) - (dq[1] - 1)]

    for i in range(len(m)):
        for j in range(dq[1]):
            head_xy = Swap(m, [i, j], tail_xy, dq)
    return m

def imprimeMatriz(m):
    for i in range(len(m)):
        print(' '.join(map(str, m[i])))
            
def exportToCSV():
    pass

if __name__== "__main__" :

    """
    dimensoes = input().strip("\n").split(" ")
    linhas = int(dimensoes[0])
    colunas = int(dimensoes[1])

    matriz = []
    for i in range(linhas):
        matriz.append(list(map(int, input().strip().split())))
    """
    print("DIMENSAO\tTEMPO(ns)")
    for i in range(1): 
        matriz = geraMatriz(999, 1000)

        #start timer
        tic = perf_counter_ns()

        #run stuff
        m = trocaQuadrantes(matriz)

        #end timer
        toc = perf_counter_ns()

        print(f"{len(m)}*{len(m[0])},{toc - tic}")

    #imprimeMatriz(m)
	