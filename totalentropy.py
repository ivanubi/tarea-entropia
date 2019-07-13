# -*- coding: utf-8 -*-

import math
from collections import Counter

def calculateEntropy(text):
    counters, lenght = Counter(text), float(len(text))
    entropy = 0
    for count in counters.values():
        entropy = entropy - (count/lenght) * math.log(count/lenght, 2)
    return entropy

# MAIN
file = open("donquijote.txt", "r")
text = file.read()

print("\nEntropia total de Shannon: " + str(calculateEntropy(text))) + "\n"
