"""Modules"""
from copy import deepcopy
from collections import defaultdict
from automatas import MealyAutomata, MoorAutomata


def from_mealy_to_moor(automata: MealyAutomata) -> MoorAutomata:
    """Transform Mealy automata to Moor automata"""
    aut = deepcopy(automata)
    unikals = set()
    for _, a in aut.table.items():
        for _, i in a.items():
            unikals.add(tuple(i))
    dt = {i:f"A{ind}" for ind,i in enumerate(unikals)}
    table_reactions = {f"A{ind}":i[1] for ind,i in enumerate(unikals)}
    table = defaultdict(dict)
    print(dt)
    for _,i in dt.items():
        for s,a in aut.table.items():
            for inp, comb in a.items():
                table[i][inp] = dt[tuple(comb)]

    state_old = list(set(i[0] for _,i in enumerate(dt.keys())))
    ind = 0
    for s,i in aut.table.items():
        if s not in state_old:
            for inp,comb in i.items():
                table[f"B{ind}"][inp] = dt[tuple(comb)]
                table_reactions[f"B{ind}"] = ""
            ind +=1
    states = list(table.keys())
    return MoorAutomata(states,states[0],aut.alphabet,table,table_reactions)
