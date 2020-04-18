import re
from time import perf_counter_ns

# Submissão Mooshak #1746

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


"""
regras das vps:
- raiz e smp preta
- novos nos sao vermelhos
- nones sao pretos
- nao pode haver 2 vermelhos consecutivos
- tem q haver # igual de nos pretos em qq caminho da
raiz para as folhas

correcoes, decididas pela cor do nó 'tia' ('aunt'):
- black aunt = Rotacao (RR, LL, LR, RL)
  -> acaba smp com 2 filhos vermelhos e um pai preto
- red aunt = ColorFlip (aplica-se a parent, aunt, child)
  -> acaba smp com 2 filhos pretos e um pai vermelho
"""

class Node:
    def __init__(self, key, value):
        self.parent = None          
        self.key = key              
        self.value = value          
        self.occurrences = [value]  
        self.is_black = False
        self.is_lc = False

        #left, right children
        self.lc, self.rc = None, None

    def insertNode(self, node):
        if self.key == node.key:
            if node.value not in self.occurrences:
                self.occurrences.append(node.value)
                return 1
        elif node.key < self.key:
            if self.lc:
                return self.lc.insertNode(node)     
            else:
                self.lc = node
                self.lc.parent = self
                self.lc.is_lc = True
                return 0
        else:
            if self.rc:
                return self.rc.insertNode(node)
            else:
                self.rc = node
                self.rc.parent = self
                self.rc.is_lc = False
                return 0

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
            print("Nó: %s   is_black: %s   Pai: %s" % (self.key, str(self.is_black), self.parent.key))
        else: print("Nó: %s   is_black: %s   Pai: None" % (self.key, str(self.is_black)))
        if self.lc != None:
            print("Filho Esquerdo de %s: %s " % (self.key, self.lc.key))
            self.lc.toString()
        if self.rc != None:
            print("Filho Direito de %s: %s" % (self.key, self.rc.key))
            self.rc.toString()

class VPTree:
    def __init__(self):
        self.root = None
        self.n_rotations = 0

    #metodos do A1.py
    def insertNode(self, node):
        """
        Inserts 'node' based on its
        lexicographic value.
        """
        if self.root:
            if self.root.insertNode(node) == 0:
                #print("inserted", node.key)
                self.checkColor(node)
                #self.printTree()
                #print()
        else:
            self.root = node
            self.root.is_black = True

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
        print("\nVP:\n-------")
        if self.root == None:
            print("Empty tree")
        else:
            self.root.toString()

    #metodos novos
    def checkColor(self, node):
        """
        Checks for violations
        in the tree.
        """
        if node == self.root:
            return
        #2 red nodes seguidos (Regra #5)
        if(node.is_black == False and node.parent.is_black == False):
            self.correctTree(node)
        self.checkColor(node.parent)

    def correctTree(self, node):
        if node.parent.is_lc == True:
            aunt = node.parent.parent.rc
            #aunt é preta -> rotacoes
            if aunt == None or aunt.is_black == True:
                self.handleRotations(node)
                return
            #aunt vermelha -> color flip
            if aunt != None and aunt.is_black == False:
                #print("CF")
                aunt.is_black = True
            node.parent.is_black = True
            node.parent.parent.is_black = False

            #root smp preta
            if node.parent.parent == self.root:
                self.root.is_black = True
            return
        if node.parent.is_lc == False:
            #aunt is node.parent.parent.lc
            aunt = node.parent.parent.lc
            if aunt == None or aunt.is_black == True:
                self.handleRotations(node)
                return
            if aunt != None and aunt.is_black == False:
                #print("CF")
                aunt.is_black = True
            node.parent.is_black = True
            node.parent.parent.is_black = False
            if node.parent.parent == self.root:
                self.root.is_black = True
            return

    def handleRotations(self, node):
        #print("ENTREI NAS ROTAÇOES:", node.key, "LC:", node.is_lc)
        #print("ESTE E O MEU PAI:", node.parent.key)
        if node.is_lc == True:
            #rr
            #if node.parent.rc:
                #print(node.parent.rc.key)
            if node.parent.is_lc == True:
                #print("RR")
                self.rr(node.parent.parent)
                self.n_rotations += 1
                #siblings = red
                node.is_black = False;
                if node.parent.rc != None:
                    node.parent.rc.is_black = False
                #parent = black
                node.parent.is_black = True
                return
            #rl
            if node.parent.is_lc == False:
                #print("RL")
                self.rr(node.parent); self.ll(node.parent);
                self.n_rotations += 2
                #node é agora pai, pai e avo antigos sao filhos
                node.is_black = False
                node.rc.is_black = True
                node.lc.is_black = True
                return
        if node.is_lc == False:
            #print(node.key, "is_lc == False")
            #ll
            if node.parent.is_lc == False:
                #print("LL")
                self.ll(node.parent.parent)
                self.n_rotations += 1
                #siblings = red
                node.is_black = False
                if node.parent.lc:
                    node.parent.lc.is_black = False
                #parent = black
                node.parent.is_black = True
                return
            #lr
            if node.parent.is_lc == True:
                #print("LR")
                #dps da ll, parent atualiza
                self.ll(node.parent);
                self.rr(node.parent);
                self.n_rotations += 2

                node.is_black = True
                node.lc.is_black = False
                node.rc.is_black = False
                return

    def countBlackNodes(self, node):
        if node == None:
            return 1;

        right_bn = countBlackNodes(node.rc)
        left_bn = countBlackNodes(node.lc)
        if right_bn != left_bn:
            print("right_bn != left_bn")
            exit;
        if node.is_black:
            left_bn += 1
        
        return left_bn

def readText(vp):
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
                vp.insertNode(new_node)
            #vp.printTree()
            #print("------")

        line_index += 1

    print("GUARDADO.")
    return vp, commands, line_index

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
    print("Linhas Time:", (total)/10**9, "s")

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
    #tic = perf_counter_ns()
    vp, commands, text_len = readText(VPTree())
    #toc = perf_counter_ns()
    #print("Time:", (toc - tic)/10**9, "s")
    #vp.printTree()
    print("# rotations:", vp.n_rotations)
    #readCommands(vp, commands, text_len)