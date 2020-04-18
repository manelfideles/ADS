import re
from time import perf_counter_ns

# Submissão Mooshak #1744

class Node:
    def __init__(self, key, value):
        self.key = key  # word
        self.value = value  # line it appears on
        self.occurrences = [value]  # record of where it appears

class WordSet:
    def __init__(self):
        self.list = []

    def searchNode(self, key):
        for node in self.list:
            if node.key == key:
                return node
        return False

    def insertNode(self, node):
        if self.list == []:
            self.list = [node]
        else:
            elem = self.searchNode(node.key)
            if elem == False:
                self.list.append(node)
            else:
                if node.value not in elem.occurrences:
                    elem.occurrences.append(node.value)

    def printSet(self):
        for node in self.list:
            print(node.key, node.occurrences)

def readText(word_set):
    """
    Reads text from terminal.
    Prints "GUARDADO." when done.
    Returns 'word_set' which is
    a list of tuples such as
    ('word', occurrences), where occurrences is a list
    with the line indexes where 'word' appears.
    """
    # word_set is a list of tuples such as
    # ('word', occurrences), where occurrences is a list
    # with the line indexes where 'word' appears

    command_set = ['LINHAS', 'ASSOC']
    commands, line = [], []
    line_index = -1

    while(line != 'TCHAU'):
        try:
            line = input()
        except EOFError:
            break;
        else:
            l = list(filter(None, re.split(r'[(),;.\s\n]\s*', line)))
            for word in l:
                if word == 'FIM' or word == 'TEXTO' or word == 'TCHAU':
                    break;
                # commands
                elif word in command_set:
                    commands.append(l)
                    break;
                # words
                else:
                    new_node = Node(word.lower(), line_index)
                    word_set.insertNode(new_node)
            line_index += 1

    print("GUARDADO.")
    # word_set.printSet()
    # print(commands)
    return word_set, commands, line_index

def readCommands(word_set, commands, text_len):
    """
    Reads command from terminal.
    """
    total = 0
    for c in commands:    
        if(c[0] == 'LINHAS' and len(c) == 2):
            #tic = perf_counter_ns()
            linhasCommand(word_set, c[1])
            #toc = perf_counter_ns()
            #total += toc - tic
        elif(c[0] == 'ASSOC' and len(c) == 3):
            tic = perf_counter_ns()
            assocCommand(word_set, c[1], c[2], text_len)
            toc = perf_counter_ns()
            total += toc - tic
        else: exit;
    print("Time: ", total/10**9, "s")

def linhasCommand(word_set, word):
    """
    Searches occurrences of 'word' 
    in the inserted text.
    Outputs the different lines where
    it occurs.
    Outputs -1 if it does not appear in the 
    text.
    Note: The search is case-insensitive
    """
    node = word_set.searchNode(word.lower())
    if node == False:
        print("-1")
    else:
        print(" ".join(map(str, node.occurrences)))

def assocCommand(word_set, word, line, text_len):
    """
    Searches occurrences of 'word' 
    in 'line'.
    Outputs "ENCONTRADA." if successful.
    Otherwise, it outputs "NAO ENCONTRADA."
    """
    if (int(line) > text_len):
        print("NAO ENCONTRADA.")
        return
    else:
        node = word_set.searchNode(word)
        if node != False and int(line) in node.occurrences:
            print("ENCONTRADA.")
        else: print("NAO ENCONTRADA.")

if __name__ == "__main__":
    #load tree
    #tic = perf_counter_ns()
    word_set, commands, text_len = readText(WordSet())
    #toc = perf_counter_ns()
    #print("Load time: ", (toc - tic)/10**9, "s")
