"""Modules"""
from itertools import combinations
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
    # Сначала построим бинарную матрицу
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
    # Теперь найдем максимальные покрытия
    res = []
    for i,a in blocks_row.items():
        for j in is_block(sorted(a), binMatrix):
            res +=[[i] + list(j)]
    final_blocks = []
    for cb in res:
        if not any(set(cb).issubset(set(other)) and cb != other for other in res):
            final_blocks.append(cb)
    print(final_blocks)

    

def get_way(a0_, a1_):
    # print(a0_, a1_)
    a0 = deepcopy(a0_)
    a1 = deepcopy(a1_)
    ans = []
    for inp, res in a0.items():
        # print(1)
        if res[0] != '-' and a1[inp][0]!='-' and  res[0]!=a1[inp][0]:
            ans.append(tuple([min(res[0],a1[inp][0]), max(res[0],a1[inp][0])]))
    return ans


@lru_cache()
def calculate(s0_, s1_, aut_:MealyAutomata):
    s0 = deepcopy(s0_)
    s1 = deepcopy(s1_)
    aut = deepcopy(aut_)
    a0 = aut.table[s0]
    a1 = aut.table[s1]
    Yav_Soot = True
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
    
    global way
    if tuple([min(s0, s1), max(s0, s1)]) in way:
        return tuple([min(s0, s1), max(s0, s1)]), 1
    else:
        way.add(tuple([min(s0, s1), max(s0, s1)]))

    coord = get_way(a0, a1)

    # print(tuple([min(s0, s1), max(s0, s1)]),"->",coord)
    ans = []
    # return tuple([min(s0, s1), max(s0, s1)]),calculate(*coord,aut)[1]
    for c in coord:
        ans.append(calculate(*c,aut)[1])
    return tuple([min(s0, s1), max(s0, s1)]), int(all(ans))


def is_block(block: list, binMatrix: dict[tuple, int]):
    incor = [i for i in combinations(block, 2) if binMatrix.get(i, 0) != 1]
    
    if not incor:
        # print(block)
        return [block]  # Возвращаем список, содержащий один корректный блок

    max_blocks = set()

    for i in block:
        temp = deepcopy(block)  # Копируем список
        temp.remove(i)  # Удаляем элемент
        new_blocks = is_block(temp, binMatrix)  # Рекурсивный вызов

        for nb in new_blocks:
            if len(nb) > 0:
                max_blocks.add(tuple(nb))  # Добавляем блок, если он такой же по размеру

    final_blocks = []
    for cb in max_blocks:
        if not any(set(cb).issubset(set(other)) and cb != other for other in max_blocks):
            final_blocks.append(cb)

    return final_blocks
