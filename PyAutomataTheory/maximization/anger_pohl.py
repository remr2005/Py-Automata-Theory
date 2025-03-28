"""Modules"""
from collections import defaultdict
from copy import deepcopy
from PyAutomataTheory.automatas import MealyAutomata

def anger_pohl(automata:MealyAutomata) -> None:
    """Anger-Pohl algorithm"""
    aut = deepcopy(automata)
    blocks = defaultdict(set)
    binMatrix = {}

    for s0, a0 in aut.table.items():
        for s1,a1 in aut.table.items():
            if s0==s1:
                continue
            
            Yav_Soot = True
            # Нахождение явного/неявного соответствия
            for inp in aut.alphabet:
                if a0[inp][1] != a1[inp][1] and a0[inp][1] != "-" and a1[inp][1] != "-":
                    binMatrix[tuple([min(s0, s1), max(s0, s1)])] = 0
                for i in range(2):
                    if not (a0[inp][i] == a1[inp][i] or a0[inp][i] == "-" or a1[inp][i] == "-"):
                        Yav_Soot = False
                        break
        
            # Эту надо отрефакторить
            if Yav_Soot:
                blocks[min(s0,s1)].add(max(s0, s1))
                binMatrix[tuple([min(s0, s1), max(s0, s1)])] = 1           
    print(binMatrix)
    print(blocks)
    # TODO: По сути, (в идеале) нужно сделать рекурентную под фунцкию, которая будет проходится по всем путям
    # TODO: Выбрасываем лишние пары(наверное стоит, можно делать это просто по ходу(а, нет скорее всего нельзая))
    # Так как наша пара
