"""Modules"""
from itertools import combinations
from collections import defaultdict
from functools import lru_cache
from copy import deepcopy
from PyAutomataTheory.automatas import MealyAutomata
from .vis import visualization
from .save_docx import save_to_docx

way = set()
text = ""

def anger_pohl(automata:MealyAutomata, num:str="") -> None:
    """Anger-Pohl algorithm"""
    aut = deepcopy(automata)
    blocks_row = defaultdict(set)
    blocks_table = defaultdict(set)
    binMatrix = {}
    global text
    # Сначала построим бинарную матрицу
    states = list(aut.table.keys())
    for i in range(len(states)):
        s0 = states[i]
        for j in range(i + 1, len(states)):  # начинаем с i+1
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
    # Теперь найдем максимальные покрытия
    res = []
    for i,a in blocks_row.items():
        for j in is_block(sorted(a), binMatrix):
            res +=[[i] + list(j)]
    final_blocks = []
    # Удалим все подмножества
    for cb in res:
        if not any(set(cb).issubset(set(other)) and cb != other for other in res):
            final_blocks.append(cb)
    
    # НУЖЕН АПРУВ СТРАТКИ ОТ ПАРМЕНОВА
    for i0,i1 in binMatrix:
        if all([not (i0 in j) for j in final_blocks]):
            final_blocks.append([i0])
        if all([not (i1 in j) for j in final_blocks]):
            final_blocks.append([i1])
    # print(binMatrix)
    # print(final_blocks)
    text+=f"Получим бинарную матрицу и итоговые блоки\n"
    # Проверка на замкнутость
    # Первоначальное разбитие
    old_states_new = {}
    new_states_old = {}
    states = []
    temp_tabel = defaultdict(dict)
    tabel_to_print = []
    tabel = defaultdict(dict)
    # Составим таблицу замкнутости
    for ind, block in enumerate(final_blocks):
        states.append(f"G{ind+1}")
        old_states_new[tuple(block)] = states[-1]
        new_states_old[states[-1]] = tuple(block)
        temp_trans = []
        temp_reac = []
        for a in aut.alphabet:
            temp_trans.append(set(tuple(aut.table[i][a][0] for i in block if aut.table[i][a][0]!="-")))
            temp_reac.append(set(tuple(aut.table[i][a][1] for i in block if aut.table[i][a][1]!="-")))
            temp_tabel[tuple(block)][a] = [temp_trans[-1], temp_reac[-1]] 
        tabel_to_print.append([f"G{ind+1}", block, *temp_trans, *temp_reac])
        # print([f"G{ind+1}", block, *temp_trans, *temp_reac])
    # Составим новый автомат
    for s, a in temp_tabel.items():
        for inp, it in a.items():
            for inp1, it1  in old_states_new.items():
                # print(inp1, it, set(inp1).issubset(it[0]))
                if it[0].issubset(set(inp1)):
                    tabel[old_states_new[s]][inp] = [it1, *it[1]]
    print(tabel_to_print)
    save_to_docx(tabel_to_print, tabel, f"otch{num}.docx", text)
    text = ""
    #  print(text)
    # print(tabel_to_print)
    # print(tabel)
        
    # Таблица с новыми состояниями
    # new_aut = MealyAutomata(states, states[0], aut.alphabet, tabel)

def get_way(a0_, a1_):
    """Возвращает найденные переходы"""
    a0 = deepcopy(a0_)
    a1 = deepcopy(a1_)
    ans = []
    for inp, res in a0.items():
        if res[0] != '-' and a1[inp][0]!='-' and  res[0]!=a1[inp][0]:
            ans.append(tuple([min(res[0],a1[inp][0]), max(res[0],a1[inp][0])]))
    return ans


@lru_cache()
def calculate(s0_, s1_, aut_:MealyAutomata):
    """Находим совместимость/несовместимость"""
    s0 = deepcopy(s0_)
    s1 = deepcopy(s1_)
    aut = deepcopy(aut_)
    a0 = aut.table[s0]
    a1 = aut.table[s1]
    Yav_Soot = True
    global text
    text += f"Начинаем с {s0, s1} "
    # Нахождение явного/неявного соответствия
    for inp in aut.alphabet:
        if a0[inp][1] != a1[inp][1] and a0[inp][1] != "-" and a1[inp][1] != "-":
            text+=f", которые явно не совместимы\n"
            return tuple([min(s0, s1), max(s0, s1)]), 0
        for i in range(2):
            if not (a0[inp][i] == a1[inp][i] or a0[inp][i] == "-" or a1[inp][i] == "-"):
                Yav_Soot = False
                break
    if Yav_Soot:
        text+=f", которые явно совместимы\n"
        return tuple([min(s0, s1), max(s0, s1)]), 1
    
    # Проверяем, не вернулись ли мы туда, где мы уже были
    global way
    if tuple([min(s0, s1), max(s0, s1)]) in way:
        text+=f", которые явно совместимы, так как встречались до этого\n"
        return tuple([min(s0, s1), max(s0, s1)]), 1
    else:
        way.add(tuple([min(s0, s1), max(s0, s1)]))

    coord = get_way(a0, a1)
    text += f"Переход из {s0, s1} -> {coord} \n"
    # проходимся по всем возможным переходам
    ans = []
    for c in coord:
        ans.append(calculate(*c,aut)[1])
    text+=f"В итоге {s0, s1} равен {int(all(ans))}\n"
    return tuple([min(s0, s1), max(s0, s1)]), int(all(ans))


def is_block(block: list, binMatrix: dict[tuple, int]):
    """Находит блоки, из данного"""
    # Находим несовместимые состояния
    global text
    incor = [i for i in combinations(block, 2) if binMatrix.get(i, 0) != 1]
    # Если таких состояний нет, то стоп
    if not incor:
        return [block]

    max_blocks = set()
    # Ищем все блоки, в которых нет несовместимых состояний
    for i in block:
        temp = deepcopy(block)
        temp.remove(i)
        new_blocks = is_block(temp, binMatrix)

        for nb in new_blocks:
            max_blocks.add(tuple(nb))
    final_blocks = []

    # Убираем все подмножества таких множеств
    for cb in max_blocks:
        if not any(set(cb).issubset(set(other)) and cb != other for other in max_blocks):
            final_blocks.append(cb)

    return final_blocks
