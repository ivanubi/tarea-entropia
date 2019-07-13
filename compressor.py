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
    '''
    Imprime en consola un diccionario en forma de tabla.
    '''
    print('{:<8} {:<8}'.format('Symbol','Times Repeated'))
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

def shannon_fano(freqs):
    '''
    Construye un árbol de código Shannon-Fano a partir
    de una lista de símbolos y sus frecuencias correspondientes.

    El árbol se almacena como un diccionario, siendo las claves
    el valor de bit (0 ó 1) y los valores el símbolo (nodo de hoja)
    u otro diccionario del mismo tipo (subárbol).
    '''
    if (len(freqs) == 2):
        # Detente cuando sólo hay dos símbolos
        # porque podemos asignar un único bit a cada uno.
        l = list(freqs.items())
        return {0: l[0], 1: l[1]}

    # Ordene los símbolos de tal manera que los símbolos de
    # frecuencia más alta estén primero.
    sorted_freqs = sorted(freqs.items(),
                          key = lambda x : x[1],
                          reverse=True)
    # Divida los símbolos en dos mitades aproximadamente iguales
    # basadas en la suma de las frecuencias. Al dividirnos,
    # tratamos de hacer que los recuentos de frecuencia total de cada mitad
    # sean lo más parecidos posible entre sí.
    first, second = split(sorted_freqs)

    # Repetir repetidamente el proceso anterior hasta llegar a
    # los nodos de la hoja (es decir, cuando sólo hay dos símbolos en
    # el resultado de una división).
    if len(freqs) > 1:
        d = {0: shannon_fano(first), 1: shannon_fano(second)}
        return d
    else:
        return freqs

def split(l):
    '''
    Divide una lista de símbolos y tuples de frecuencias en
    dos mitades con un recuento de frecuencias lo más cercano
    posible a cada una de ellas.
    '''

    # Calcular el número total de frecuencias
    # para las mitades cuando se combinan.
    total = sum([prob for _, prob in l])

    first_half = {}
    second_half = {}

    # Queremos que cada mitad de la frecuencia total
    # cuente lo más cerca posible de la mitad de la frecuencia total.
    half = total / 2
    count = 0

    # Flag para indicar cuándo pasar a la segunda mitad
    first_half_done = False

    for entry in l:
        symbol, prob = entry

        if count >= half:
            # Tenemos una mitad que es lo más cercana posible a
            # nuestra aproximación de conteo de frecuencia para
            # cada mitad - pasar a la segunda mitad.
            first_half_done = True

            second_half[symbol] = prob
        else:
            if not first_half_done:
                first_half[symbol] = prob
            else:
                second_half[symbol] = prob

        count += prob

    return first_half, second_half

def dict_to_table(d, l={}, code=''):
    '''
    Helper para convertir el árbol de código Shannon-Fano
    en una tabla que puede ser indexada por símbolo para
    recuperar el código SF para ese símbolo.
    '''
    for k, v in d.items():
        if isinstance(v, dict):
            # Hay un subárbol
            dict_to_table(v, l, code + str(k))
        else:
            # Hemos llegado a un nodo de hoja - añadir el símbolo
            # y su código en la tabla
            if isinstance(v, float):
                symbol = k
                l[symbol] = code
                return l
            symbol = v[0]
            l[symbol] = code + str(k)

    return l

# MAIN
file = open("donquijote.txt", "r")
text = file.read()
counters = Counter(text)
#DEBUGGING PURPOSES: printDictAsATable(counters)
frequencies = calculateFrequencies( counters )
#printDictAsATable(frequencies)

# Crear el arbol Shannon-Fano
d = shannon_fano(frequencies)
#DEBUGGING PURPOSES: print(d)
# ... y construir una tabla de codigos a partir del arbol
table = dict_to_table(d)

#print("\nTabla de codigos computados:")
#for k in sorted(table.keys()):
#    print('{} => {}'.format(k, table[k]))

# Codifica el texto dado con la tabla de códigos
compresedText = ""

for c in text:
    compresedText += table[c]

realShannonFanoCompression = (len(compresedText)/float(len(text)*8))*8

print("\nCompresion teórica de Shannon: " + str(calculateEntropy(text)))
print("Compresion real mediante Shannon-Fano: " + str( realShannonFanoCompression ))
print("Cantidad de bits utilizados en el texto original: " + str(len(text)*8) )
print("Cantidad de bits utilizados en el texto comprimido: " + str(len(compresedText)) )
print("Texto comprimido en un " + str( round( (realShannonFanoCompression/8)*100, 3)) + "%\n")
