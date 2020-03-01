"""
Input:
9 -> tamanho da seq (n)
1 2 3 4 5 6 7 8 9 -> seq
O objetivo é devolver um elemento
que apareca em seq mais
do que n>2 vezes
Se nao houver nenhum, devolver
"Sem elemento"
"""
from random import randint
from time import perf_counter_ns

def randomLengthVector(l, u):
    n = randint(l, u)
    seq = [randint(l, u) for i in range(n)]
    return n, seq if n != 0 else None

def getInput():
    seq = list(map(int, input().strip().split()))
    return seq

def getMajorityElement(n, seq):
    counter = 0
    current = None
    for elem in seq:
        if counter != 0:
            if current == elem:
                counter +=1
            else: counter -= 1
            #counter += 1 if current == elem else -1
        else: # counter == 0
            current = elem
            counter = 1

    # check for majority
    if (seq.count(current) > n // 2):
         return current
    else: None

def test(x, l, u):
    """
    x -> iterations
    l -> lower bound for the size of the array
    u -> upper bound for the size of the array

    Measures the time it takes
    to perform the algorithm

    Outputs the length and measured
    time to a csv
    """
    for i in range(x):
        n, seq = randomLengthVector(l, u)
        print(n, seq)

        tic = perf_counter_ns()

        #run stuff
        maj = getMajorityElement(n, seq)

        #end timer
        toc = perf_counter_ns()

        print(f"{n},{toc - tic}")

        with open("majority_out.txt", 'a') as f:
            f.write(f"{n},{toc - tic}\n")

if __name__ == "__main__":
    test(1000, 5000, 10000)
