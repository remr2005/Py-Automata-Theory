"""Modules"""
from collections import defaultdict
from functools import lru_cache
from copy import deepcopy
from PyAutomataTheory.automatas import MealyAutomata

way = set()

def anger_pohl(automata:MealyAutomata) -> None:
    """Anger-Pohl algorithm"""
    aut = deepcopy(automata)
    blocks_row = defaultdict(set)
    blocks_table = defaultdict(set)
    binMatrix = {}    
    for s0, a0 in aut.table.items():
        for s1,a1 in aut.table.items():
            if s0==s1:
                continue
            min_s = min(s0,s1)
            max_s = max(s0,s1)


            c, r = calculate(min_s, max_s, aut)
            global way
            way = set()
            binMatrix[c] = r
            if r == 0:
                print(c)
            if r:
                blocks_row[min_s].add(max_s)
                blocks_table[max_s].add(min_s)
    calculate.cache_clear()
    # print(binMatrix)
    # print(blocks_row)
    # print(blocks_table)
    

def get_way(a0_, a1_):
    # print(a0_, a1_)
    a0 = deepcopy(a0_)
    a1 = deepcopy(a1_)
    for inp, res in a0.items():
        print(1)
        if res[0] != '-' and a1[inp][0]!='-':
            return tuple([min(res[0],a1[inp][0]), max(res[0],a1[inp][0])])


@lru_cache()
def calculate(s0_, s1_, aut_:MealyAutomata):
    s0 = deepcopy(s0_)
    s1 = deepcopy(s1_)
    aut = deepcopy(aut_)
    a0 = aut.table[s0]
    a1 = aut.table[s1]
    Yav_Soot = True
    global way
    if tuple([min(s0, s1), max(s0, s1)]) in way:
        return tuple([min(s0, s1), max(s0, s1)]), 1
    else:
        way.add(tuple([min(s0, s1), max(s0, s1)]))
    # Нахождение явного/неявного соответствия
    for inp in aut.alphabet:
        if a0[inp][1] != a1[inp][1] and a0[inp][1] != "-" and a1[inp][1] != "-":
            return tuple([min(s0, s1), max(s0, s1)]), 0
        for i in range(2):
            if not (a0[inp][i] == a1[inp][i] or a0[inp][i] == "-" or a1[inp][i] == "-"):
                Yav_Soot = False
                break
    if Yav_Soot:
        return tuple([min(s0, s1), max(s0, s1)]), 1

    coord = get_way(a0, a1)

    return tuple([min(s0, s1), max(s0, s1)]),calculate(*coord,aut)[1]