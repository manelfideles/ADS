import re
from time import perf_counter_ns

# Submissão Mooshak #1745

# adaptado de:

# Rob Edwards
# https://www.youtube.com/user/RobEdwardsSDSU/

# Brian Faure
# https://www.youtube.com/user/bluboy12345

# stackoverflow.com,
# https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
# https://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin

# softwareengineering.stackexchange.com
# https://softwareengineering.stackexchange.com/questions/201765/reason-for-return-statement-in-recursive-function-call

# Ammar Al-Nasseri
# https://derka.space/RefrencePage/DataStructuresZy/balanced_trees/AVL_Trees/balanced_trees_AVL_Trees_s5.php

# Data Structures - A.A.Puntambekar
# https://books.google.pt/books?id=lEJtDKJ2dkoC&printsec=frontcover&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false

# Universidade de São Paulo:
# https://www.ime.usp.br

# Documentação do Python:
# https://python-reference.readthedocs.io/

class Node:
    #constructor
    def __init__(self, key, value):
        self.parent = None          #parent node
        self.key = key              #word
        self.value = value          #line it appears on
        self.occurrences = [value]  #record of where it appears
        self.height = 1             #height of the node

        #left, right children
        self.lc, self.rc = None, None

    def insertNode(self, node):
        if self.key == node.key:
            if node.value not in self.occurrences:
                self.occurrences.append(node.value)
        elif node.key < self.key:
            if self.lc:
                self.lc.insertNode(node)        
            else:
                self.lc = node
                self.lc.parent = self
        else:
            if self.rc:
                self.rc.insertNode(node)
            else:
                self.rc = node
                self.rc.parent = self

    def searchNode(self, key):
        if self.key == key:
            return self
        elif key < self.key:
            if self.lc:
                return self.lc.searchNode(key)
            else:
                return False
        else:
            if self.rc:
                return self.rc.searchNode(key)
            else:
                return False

    def toString(self):
        if self.parent != None:
            print("Nó: " + self.key, "   Pai: " + self.parent.key)
        else: print("Nó: " + self.key, "   Pai: None")
        if self.lc != None:
            print("Filho Esquerdo de %s: %s " % (self.key, self.lc.key))
            self.lc.toString()
        if self.rc != None:
            print("Filho Direito de %s: %s" % (self.key, self.rc.key))
            self.rc.toString()
   
class AVLTree:
    #constructor
    def __init__(self):
        """
        Returns NULL root node
        """
        self.root = None
        self.n_rotations = 0
    
    def insertNode(self, node):
        """
        Inserts 'node' based on its
        lexicographic value.
        """
        if self.root:
            self.root.insertNode(node)
            self.findFirstUnbalancedNode(node, [])
        else:
            self.root = node

    def getHeight(self, node):
        if node == None:
            return 0
        else:
            return node.height

    def balanceFactor(self, node):
        if not node:
            return 0
        else:
            return abs(self.getHeight(node.lc) - self.getHeight(node.rc))

    def findFirstUnbalancedNode(self, node, path):
        """
        Traverse upwards from the
        recently inserted 'node' to check
        for inbalances.
        Returns a list with the path
        of traversal from 'node' to
        the unbalanced node.
        """
        #if node == root
        if node.parent == None:
            return
        path = [node] + path

        #lh = self.getHeight(node.parent.lc)
        #rh = self.getHeight(node.parent.rc)
        #balance_factor = abs(lh - rh)
        balance_factor = self.balanceFactor(node.parent)
        #print(balance_factor)

        if balance_factor == 2:
            #print("Rebalancing needed!")
            path = [node.parent] + path
            if len(path) < 3:
                print((node.key, node.value), [node.key for node in path])
                raise Exception('len(path) < 2')
            self.balanceTree(path[:3])
            return

        new_height = node.height + 1
        if new_height > node.parent.height:
            node.parent.height = new_height

        self.findFirstUnbalancedNode(node.parent, path)

    def balanceTree(self, path):
        """
        Defines what rotations to do
        given a 'path'
        """
        #print("Rebalancing tree...")
        avo, pai, filho = path[0], path[1], path[2]
        #print("path:", avo.key, pai.key, filho.key)

        if filho == pai.rc and pai == avo.rc:
            #print("LL")
            self.ll(avo)
            self.n_rotations += 1
        elif filho == pai.lc and pai == avo.lc:
            #print("RR")
            self.rr(avo)
            self.n_rotations += 1
        elif filho == pai.lc and pai == avo.rc:
            #print("RL")
            self.rr(pai); self.ll(avo)
            self.n_rotations += 2
        else:
            #print("LR")
            self.ll(pai); self.rr(avo)
            self.n_rotations += 2
        
    def rr(self, node):
        """
        Performs right rotation of 'node'.
        """
        subroot = node.parent #desligar a subtree da arvore
        k2 = node.lc

        k2rc = k2.rc #guardar o lc de k2
        k2.rc = node

        node.parent = k2
        node.lc = k2rc #o rc de node é o antigo lc de k2
        if k2rc != None:
            k2rc.parent = node
        k2.parent = subroot #religar subtree
        if k2.parent == None:
            self.root = k2
        else:
            if k2.parent.lc == node:
                k2.parent.lc = k2
            else:
                k2.parent.rc = k2
        
        node.height = 1 + max(self.getHeight(node.lc), self.getHeight(node.rc))
        k2.height = 1 + max(self.getHeight(k2.lc), self.getHeight(k2.rc))
        
    def ll(self, node):
        """
        Performs left rotation of 'node'.
        """
        subroot = node.parent #desligar a subtree da arvore
        k2 = node.rc

        k2lc = k2.lc #guardar o lc de k2
        k2.lc = node

        node.parent = k2
        node.rc = k2lc #o rc de node é o antigo lc de k2
        if k2lc != None:
            k2lc.parent = node

        k2.parent = subroot #religar subtree
        if k2.parent == None:
            self.root = k2
        else:
            if k2.parent.lc == node:
                k2.parent.lc = k2
            else:
                k2.parent.rc = k2

    def searchNode(self, key):
        """
        Searches node in AVL tree.
        Returns 0 if in tree
        Returns the line(s) where 'node'
        occurs.
        """
        if self.root:
            return self.root.searchNode(key)
        else: return False

    def printTree(self):
        """
        Prints tree in preorder.
        """
        print("\nAVL:\n-------")
        if self.root == None:
            print("Empty tree")
        else:
            self.root.toString()

def readText(avl):
    """
    Reads text from terminal.
    Prints "GUARDADO." when done.
    Outputs populated tree and
    the commands to be executed.
    """
    #word_set is a list of tuples such as
    #('word', occurrences), where occurrences is a list
    #with the line indexes where 'word' appears

    command_set = ['LINHAS', 'ASSOC']
    commands, line = [], []
    line_index = -1

    while(line != 'TCHAU'):
        line = input()
        l = list(filter(None, re.split(r'[(),;.\s\n]\s*', line)))
        for word in l:
            if word == 'FIM' or word == 'TEXTO' or word == 'TCHAU':
                break;
            #commands
            elif word in command_set:
                commands.append(l)
                break;
            #words
            else:
                new_node = Node(word.lower(), line_index)
                avl.insertNode(new_node)
        line_index += 1

    print("GUARDADO.")
    #word_set.printSet()
    #print(commands)
    return avl, commands, line_index

def readCommands(tree, commands, text_len):
    """
    Reads command from terminal.
    """
    total = 0
    for c in commands:    
        if(c[0] == 'LINHAS' and len(c) == 2):
            tic = perf_counter_ns()
            linhasCommand(tree, c[1])
            toc = perf_counter_ns()
            total += toc - tic
        elif(c[0] == 'ASSOC' and len(c) == 3):
            #tic = perf_counter_ns()
            assocCommand(tree, c[1], c[2], text_len)
            #toc = perf_counter_ns()
            #total += toc - tic
        else: exit;
    print("Time: ", total/10**9, "s")

def linhasCommand(tree, word):
    """
    Searches occurrences of 'word' 
    in the inserted text.
    Outputs the different lines where
    it occurs.
    Outputs -1 if it does not appear in the 
    text.
    Note: The search is case-insensitive
    """
    node = tree.searchNode(word.lower())
    if node == False:
        print("-1")
    else:
        print(" ".join(map(str, node.occurrences)))

def assocCommand(tree, word, line, text_len):
    """
    Searches occurrences of 'word' 
    in 'line'.
    Outputs "ENCONTRADA." if successful.
    Otherwise, it outputs "NAO ENCONTRADA."
    """
    #x = 0
    if (int(line) > text_len):
        print("NAO ENCONTRADA.")
        return
    else:
        node = tree.searchNode(word)
        if node != False and int(line) in node.occurrences:
            print("ENCONTRADA.")
        else: print("NAO ENCONTRADA.")

if __name__ == "__main__":

    # Os testes foram feitos com a função perf_counter_ns
    # do módulo time. Para cada operação que exigisse a criação de
    # uma lista de palavras, a mesma foi gerada com o método sample
    # do módulo random. Essa lista foi depois usada nas medições
    # dos tempos de execução da operação, em todas as implementações
    # para reduzir o número de variáveis durante as mesmas.
    # Os textos originais foram alterados com as respetivas
    # listas para poder executar as diferentes operações.
    # A unidade escolhida foi o segundo (s), pois facilita a
    # avaliação dos resultados e deteção de problemas nas medições.
    # No método readCommand, as ferramentas de medição estão comentadas
    # e eram descomentadas conforme necessário.

    tic = perf_counter_ns()
    avl, commands, text_len = readText(AVLTree())
    toc = perf_counter_ns()
    print("Time: ", (toc - tic)/10**9, "s")
    #readCommands(avl, commands, text_len)

    print("# of rotations: ", avl.n_rotations)