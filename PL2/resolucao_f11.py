#f1.1 AED

def A(seq, n, valor):
    """
    seq -> sequencia inserida
    n -> comprimento subsquencia
    valor -> soma a procurar
    """
    for i in range(n):
        for j in range(n):
            soma = 0
            for z in range(i, j):
                soma += seq[z]
            if(soma == valor):
                print(f"SUBSEQUENCIA EXISTE NA POSICAO {i}")
                return 0
    print("SUBSEQUENCIA NAO EXISTE")
    return 1

def B(seq, n, valor):
    """
    seq -> sequencia inserida
    n -> comprimento subsquencia
    valor -> soma a procurar
    """
    for i in range(n):
        soma = 0
        for j in range(n):
            soma += seq[j]
            if(soma == valor):
                print(f"SUBSEQUENCIA EXISTE NA POSICAO {i}")
                return 0
    print("SUBSEQUENCIA NAO EXISTE")
    return 1

def C(seq, n, valor):
    """
    seq -> sequencia inserida
    n -> comprimento subsquencia
    valor -> soma a procurar
    """
    for i in range(n):
        soma = 0
        j = i
        while((soma < valor) and (j <= n)):
            soma += seq[j]
            if(soma == valor):
                print(f"SUBSEQUENCIA EXISTE NA POSICAO {i}")
                return 0
            j += 1
    print("SUBSEQUENCIA NAO EXISTE")
    return 1

def D(seq, n, valor):
    """
    seq -> sequencia inserida
    n -> comprimento subsquencia
    valor -> soma a procurar
    """
    soma = 0
    i, j = 1, 1
    while((soma != valor) and (i <= n)):
        while((soma < valor) and (j <= n)):
            soma += seq[j]
            if(soma == valor):
                print(f"SUBSEQUENCIA EXISTE NA POSICAO {i}")
                return 0
            j += 1
        soma -= seq[i]
        i = j + 1
    if(soma == valor):
        print(f"SUBSEQUENCIA EXISTE NA POSICAO {i+1}")
        return 0
    else: 
        print("SUBSEQUENCIA NAO EXISTE")
        return 1


