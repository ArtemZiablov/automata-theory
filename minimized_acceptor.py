import copy
import random
from math import *


def alphabet_from_dict(d: dict) -> list:
    alph = list()
    temp = list(d.values())
    for d in temp:
        temp1 = list(d.keys())
        for a in temp1:
            if len(a) == 1 and a not in alph:
                alph.append(a)
    # print(alph)
    return alph


def table_output(table: list):
    print("Table:")
    for i in range(len(table)):  # 1 step
        for j in range(len(table)):
            if table[i][j] is not True and table[i][j] is not False:
                print(f"{table[i][j]}\t", end="")
            else:
                print(table[i][j], end="    ")
        print("\n")


def dict_output(d):
    for i in d:  # вивід словника
        print(i, ":")
        for j in d[i]:
            print('\t', j, " : ", d[i][j])
    print()


class Acceptor:
    def __init__(self, spec: dict):
        self._alphabet = alphabet_from_dict(spec)  #
        self._doDict = spec  #

    def get_alphabet(self):
        return self._alphabet

    def get_dict(self):
        return self._doDict

    def run(self, state, u):
        if u:
            a, u_new = u[0], u[1:]
            return self.run(self._doDict[state][a], u_new)
        return state

    def isAcceptable(self, u):
        return self._doDict[self.run(0, u)]['acceptant']


def run(d, state, a):
    return d[state][a]


def do_table(d):
    A = alphabet_from_dict(d)  # алфавіт
    Q = list(d.keys())         # стани
    k, l = len(Q), len(Q)
    table = [[0] * k for i in range(l)]

    for i in range(k):  # 1 step
        for j in range(l):
            if 0 <= i < j < l:
                table[i][j] = d[i]['acceptant'] != d[j]['acceptant']
    while True:  # 2 step
        ic = 0   # 2.1
        for i in range(k):
            for j in range(l):
                if 0 <= i < j <= l and table[i][j] == False:  # 2.2
                    for a in A:                               # 2.2.1
                        _k = min(run(d, i, a), run(d, j, a))  # 2.2.1.1
                        _l = max(run(d, i, a), run(d, j, a))
                        if table[_k][_l]:                     # 2.2.1.2
                            ic += 1
                            table[i][j] = table[_k][_l]
        if ic == 0:  # 2.3
            break
    return table


def get_groups(table):
    groups = list()  # пары различимых состояний
    groups_check = list()
    groups_res = list()  # список взаємно еквівалентних блоків
    for i in range(len(table)):
        for j in range(len(table)):
            if 0 <= i < j <= len(table) and table[i][j] == False:
                groups_check.append(i), groups_check.append(j)
                groups.append([i, j])
    print(f"Groups of equivalent states: {groups}")
    for i in range(len(table)):
        if i not in groups_check:
            groups_res.append([i])
    for i in range(len(groups)):  # формуємо блоки взаємно еквівалентних станів
        index = min(groups[i][0], groups[i][1])
        groups_res.insert(index, groups[i])
    print("Blocks of mutually equivalent states: ", groups_res)
    return groups_res


def create_dict(d: dict, groups: list):
    # Створюємо нові стани для кожної групи еквівалентності.
    new_states = {state: i for i, group in enumerate(groups) for state in group}
    print("%%%%%%%%%%  ", new_states)
    # Оновлюємо функцію переходу.
    new_spec = {}
    for state, transitions in d.items():
        # Створюємо новий стан для поточного стану згідно з групою еквівалентності.
        new_state = new_states[state]
        print("new_state: ", new_state)
        # Створюємо новий символ переходу та новий стан відповідно до групи еквівалентності.
        # Виняток складає символ 'acceptant', який переносимо без змін.
        new_transitions = {symbol: new_states.get(target, None) for symbol, target in transitions.items() if symbol != 'acceptant'}
        print("new_transitions: ", new_transitions)
        new_transitions['acceptant'] = transitions.get('acceptant', None)
        # Додаємо новий стан з оновленою функцією переходу до нового словника.
        new_spec[new_state] = new_transitions

    return new_spec  # повертаємо словник


def acceptor_reduction(d: dict):
    print("Acceptor before minimization:")
    dict_output(d)                          # вивід початкового акцептора
    table = do_table(d)                     # створення таблиці не еквівалентності станів
    table_output(table)                     # вивід таблиці
    groups = get_groups(table)              # отримання блоків взаємно еквівалентних станів
    minimized_acc = create_dict(d, groups)  # створення словника мінімізованого акцептора
    print("Acceptor after minimization:")
    dict_output(minimized_acc)              # вивід акцептора
    return minimized_acc


def source(n, alphabet):
    ic = 0
    while True:
        if ic < n:
            ic += 1
            yield random.choice(alphabet)
        else:
            return


d1 = {
    0: {'a': 1, 'b': 0, 'acceptant': True},
    1: {'a': 0, 'b': 2, 'acceptant': False},
    2: {'a': 0, 'b': 1, 'acceptant': False}
}

d_1 = acceptor_reduction(d1)
A = Acceptor(d1)
B = Acceptor(d_1)

for noex in range(10):
    s = source(10, ''.join(A.get_alphabet()))
    u = ""
    for a in s:
        u += a
    print(f"Experiment {noex + 1}:\n'{u}' is"
          f"\n\t {'acceptable' if B.isAcceptable(u) else 'not acceptable'} by A and"
          f"\n\t {'acceptable' if A.isAcceptable(u) else 'not acceptable'} by B")

d2 = {
    0: {'a': 1, 'b': 2, 'acceptant': False},
    1: {'a': 3, 'b': 1, 'acceptant': False},
    2: {'a': 2, 'b': 3, 'acceptant': False},
    3: {'a': 4, 'b': 5, 'acceptant': True},
    4: {'a': 3, 'b': 4, 'acceptant': False},
    5: {'a': 4, 'b': 5, 'acceptant': True}
}

d_2 = acceptor_reduction(d2)
C = Acceptor(d2)
D = Acceptor(d_2)

for noex in range(10):
    s = source(10, ''.join(C.get_alphabet()))
    u = ""
    for a in s:
        u += a
    print(f"Experiment {noex + 1}:\n'{u}' is"
          f"\n\t {'acceptable' if C.isAcceptable(u) else 'not acceptable'} by C and"
          f"\n\t {'acceptable' if D.isAcceptable(u) else 'not acceptable'} by D")
