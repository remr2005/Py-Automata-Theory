"""Code for Pi-minimization algorithm"""
from collections import defaultdict
from copy import deepcopy
from automatas import MealyAutomata

def pi_minimization(automata_: MealyAutomata) -> MealyAutomata:
    """Pi-minimization algorithm for Mealy automaton"""
    automata = deepcopy(automata_)

    # Construct transition and reaction tables
    table_trans = {s: {a_n: i[0] for a_n, i in a.items()} for s, a in automata.table.items()}
    table_react = {s: {a_n: i[1] for a_n, i in a.items()} for s, a in automata.table.items()}

    # Find unique reaction columns
    unique_reactions = list(set(tuple(j for _, j in a.items()) for _, a in table_react.items()))

    # Group states by their reactions
    reactions = defaultdict(dict)
    reactions_ = {}
    for s, a in deepcopy(table_react).items():
        try:
            ind = unique_reactions.index(tuple(react for _, react in a.items()))
            reactions[ind][s] = a
            reactions_[s] = ind
        except ValueError:
            continue

    # Start state partitioning and minimization
    ind_char = 65  # ASCII code for 'A'
    while True:
        temp_reactions = defaultdict(dict)
        temp_reactions_ = {}

        for _, group in reactions.items():
            # Refine partitions based on transitions
            for s, a in group.items():
                for inp in a:
                    group[s][inp] = reactions_[table_trans[s][inp]]
            unique_reactions = list(set(tuple(j for _, j in a.items()) for _, a in group.items()))

            for s, a in group.items():
                try:
                    ind = unique_reactions.index(tuple(react for _, react in a.items()))
                    temp_reactions[f"{chr(ind_char)}{ind}"][s] = a
                    temp_reactions_[s] = f"{chr(ind_char)}{ind}"
                except IndexError:
                    continue
            ind_char += 1

        # If partitioning remains unchanged, stop
        if len(temp_reactions.keys()) == len(reactions.keys()):
            break
        reactions = temp_reactions
        reactions_ = temp_reactions_

    # Restore initial states and remove equivalent states
    dt = {}
    dt_ = {}
    for s, a in reactions.items():
        k = list(a.keys())[0]
        dt[k] = a[k]
        dt_[s] = k

    # Update transitions with new state names
    for s, a in dt.items():
        for inp, tran in a.items():
            dt[s][inp] = [dt_[tran], table_react[s][inp]]

    # Update automaton with minimized states and transitions
    automata.states = list(dt.keys())
    automata.state = automata.states[0]
    automata.table = dt

    return automata
