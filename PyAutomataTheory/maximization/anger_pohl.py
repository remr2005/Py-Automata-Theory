"""Modules"""
from itertools import combinations
from collections import defaultdict
from functools import lru_cache
from copy import deepcopy
from PyAutomataTheory.automatas import MealyAutomata


way = set()
text = ""


def anger_pohl(automata: MealyAutomata, num: str = "") -> tuple[MealyAutomata,list]:
    """Anger-Pohl algorithm — минимизация автомата Мили"""
    aut = deepcopy(automata)
    blocks_row = defaultdict(set)
    blocks_table = defaultdict(set)
    binMatrix = {}
    global text
    # print(automata.table)
    # Строим бинарную матрицу совместимости пар состояний
    states = list(aut.table.keys())
    for i in range(len(states)):
        s0 = states[i]
        for j in range(i + 1, len(states)):
            s1 = states[j]
            min_s = min(s0, s1)
            max_s = max(s0, s1)

            c, r = calculate(min_s, max_s, aut)
            global way
            way = set()
            binMatrix[c] = r
            if r:
                blocks_row[min_s].add(max_s)
                blocks_table[max_s].add(min_s)

    calculate.cache_clear()

    # Ищем максимальные блоки совместимых состояний
    res = []
    for i, a in blocks_row.items():
        for j in is_block(sorted(a), binMatrix):
            res.append([i] + list(j))

    # Удаляем все подмножества блоков
    final_blocks = []
    for cb in res:
        if not any(set(cb).issubset(set(other)) and cb != other for other in res):
            final_blocks.append(cb)

    # Добавляем одиночные состояния, не входящие ни в один блок
    for i0, i1 in binMatrix:
        if all(i0 not in j for j in final_blocks):
            final_blocks.append([i0])
        if all(i1 not in j for j in final_blocks):
            final_blocks.append([i1])

    text += "Получим бинарную матрицу и итоговые блоки\n"

    # Построение таблицы замкнутости
    old_states_new = {}
    new_states_old = {}
    states = []
    temp_tabel = defaultdict(dict)
    tabel_to_print = []
    tabel = defaultdict(dict)

    # Формируем новые состояния G1, G2, ...
    for ind, block in enumerate(final_blocks):
        state_name = f"G{ind + 1}"
        states.append(state_name)
        old_states_new[tuple(block)] = state_name
        new_states_old[state_name] = tuple(block)
        temp_trans = []
        temp_reac = []
        for a in aut.alphabet:
            transitions = set(aut.table[i][a][0] for i in block if aut.table[i][a][0] != "-")
            reactions = set(aut.table[i][a][1] for i in block if aut.table[i][a][1] != "-")
            temp_trans.append(transitions)
            temp_reac.append(reactions)
            temp_tabel[tuple(block)][a] = [transitions, reactions]
        tabel_to_print.append([state_name, block, *temp_trans, *temp_reac])

    # Строим таблицу переходов нового автомата
    for s, a in temp_tabel.items():
        for inp, it in a.items():
            for inp1, it1 in old_states_new.items():
                if it[0].issubset(set(inp1)):
                    tabel[old_states_new[s]][inp] = [it1, *it[1]]

    text = ""
    print(minimize_cover(final_blocks, automata))
    return MealyAutomata(states, states[0],automata.alphabet, tabel), final_blocks


def minimize_cover(max_cover, automata):
    """Находит минимальное покрытие"""
    S = set(automata.states)
    candidate_blocks = [set(block) for block in max_cover]
    for r in range(1, len(candidate_blocks) + 1):
        for comb in combinations(candidate_blocks, r):
            # Если в нов
            if set().union(*comb) == S:
                if is_zamk(list(comb), automata):
                    return list(comb)
    return max_cover


def is_zamk(blocks, aut) -> bool:
    """проверяет покрытие на замкнутость"""
    for ind, block in enumerate(blocks):
        for a in aut.alphabet:
            transitions = set(aut.table[i][a][0] for i in block if aut.table[i][a][0] != "-")
            if not transitions:  # Если нет переходов по этому символу
                continue 
            found = any(transitions.issubset(other_block) for other_block in blocks)
            if not found:
                return False
    return True


def get_way(a0_, a1_):
    """Возвращает пары переходов, где состояния различаются"""
    a0 = deepcopy(a0_)
    a1 = deepcopy(a1_)
    return [(min(res[0], a1[inp][0]), max(res[0], a1[inp][0])) 
            for inp, res in a0.items() 
            if res[0] != '-' and a1[inp][0] != '-' and res[0] != a1[inp][0]]


@lru_cache()
def calculate(s0_, s1_, aut_: MealyAutomata):
    """Проверяет, являются ли состояния s0 и s1 совместимыми"""
    s0 = deepcopy(s0_)
    s1 = deepcopy(s1_)
    aut = deepcopy(aut_)
    a0 = aut.table[s0]
    a1 = aut.table[s1]
    Yav_Soot = True
    global text
    text += f"Начинаем с {s0, s1} "

    # Проверка на явную несовместимость (по выходам)
    for inp in aut.alphabet:
        if a0[inp][1] != a1[inp][1] and a0[inp][1] != "-" and a1[inp][1] != "-":
            text += f", которые явно не совместимы\n"
            return (min(s0, s1), max(s0, s1)), 0
        for i in range(2):
            if not (a0[inp][i] == a1[inp][i] or a0[inp][i] == "-" or a1[inp][i] == "-"):
                Yav_Soot = False
                break

    if Yav_Soot:
        text += f", которые явно совместимы\n"
        return (min(s0, s1), max(s0, s1)), 1

    # Проверка на повторное появление пары
    global way
    pair = (min(s0, s1), max(s0, s1))
    if pair in way:
        text += f", которые явно совместимы, так как встречались до этого\n"
        return pair, 1
    
    way.add(pair)
    coord = get_way(a0, a1)
    text += f"Переход из {s0, s1} -> {coord} \n"
    ans = all(calculate(*c, aut)[1] for c in coord)
    text += f"В итоге {s0, s1} равен {int(ans)}\n"
    return pair, int(ans)


def is_block(block: list, binMatrix: dict[tuple, int]):
    """Рекурсивно находит все подмножества блока, в которых все состояния совместимы"""
    global text
    # Находим несовместимые пары
    incor = [i for i in combinations(block, 2) if binMatrix.get(i, 0) != 1]
    if not incor:
        return [block]

    max_blocks = set()
    for i in block:
        temp = deepcopy(block)
        temp.remove(i)
        new_blocks = is_block(temp, binMatrix)
        for nb in new_blocks:
            max_blocks.add(tuple(nb))

    final_blocks = []
    for cb in max_blocks:
        if not any(set(cb).issubset(set(other)) and cb != other for other in max_blocks):
            final_blocks.append(cb)

    return final_blocks
