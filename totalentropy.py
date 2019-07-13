# -*- coding: utf-8 -*-

import math
from collections import Counter

def calculateEntropy(text):
    counters, lenght = Counter(text), float(len(text))
    entropy = 0
    for count in counters.values():
        entropy = entropy - (count/lenght) * math.log(count/lenght, 2)
    return entropy

def printDictAsATable(dic):
    print('\n{:<8} {:<8}'.format('Symbol','Times Repeated'))
    for symbol, times_repeated in dic.items():
        print('{:<8} {:<8}'.format(symbol, times_repeated))

def calculateFrequencies(dic):
    '''
    Recibe un diccionario con los símbolos y frecuencia de los
    los símbolos y devuelve un diccionario con los símbolos y el
    porcentaje de veces que aparecen en el texto.
    '''
    total_times_repeated = 0

    for symbol in dic:
        total_times_repeated = total_times_repeated + dic[symbol]

    for symbol in dic:
        dic[symbol] = float(dic[symbol]) / total_times_repeated
    return(dic)

# MAIN
file = open("donquijote.txt", "r")
text = file.read()
counters = Counter(text)
#printDictAsATable(counters)
frequencies = calculateFrequencies( counters )
#printDictAsATable(frequencies)

print("\nEntropia total de Shannon: " + str(calculateEntropy(text))) + "\n"
