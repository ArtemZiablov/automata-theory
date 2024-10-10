import copy
import random

def isLetter(x):
    return isinstance(x, str) and len(x) == 1

class ReX:

    def __init__(self):
        self._data = None

    @staticmethod
    def create(what, *using):
        if not isinstance(what, str):
            raise Exception("string is expected")
        if what == "empty":
            return EmptyReX()
        if what == 'nil':
            return NilReX()
        if what == 'letter':
            if len(using) == 1:
                return SingleReX(*using)
            raise Exception("invalid ReX specification")
        if what == 'alt':
            if len(using) == 2:
                if isinstance(using[0], EmptyReX):
                    if isinstance(using[1], ReX):
                        return copy.deepcopy(using[1])
                    raise Exception("invalid ReX specification")
                if isinstance(using[1], EmptyReX):
                    if isinstance(using[0], ReX):
                        return copy.deepcopy(using[0])
                    raise Exception("invalid ReX specification")
                return AltReX(*using)
            raise Exception("invalid ReX specification")
        if what == 'cat':
            if len(using) == 2:
                if (isinstance(using[0], EmptyReX) or isinstance(using[1], EmptyReX)):
                    return EmptyReX()
                if (isinstance(using[0], NilReX)):
                    if isinstance(using[1], ReX):
                        return copy.deepcopy(using[1])
                    raise Exception("invalid ReX specification")
                if (isinstance(using[1], NilReX)):
                    if isinstance(using[0], ReX):
                        return copy.deepcopy(using[0])
                    raise Exception("invalid ReX specification")
                return CatReX(*using)
            raise Exception("invalid ReX specification")
        if what == 'star':
            if len(using) == 1:
                if (isinstance(using[0], EmptyReX) or isinstance(using[0], NilReX)):
                    return NilReX()
                if isinstance(using[0], StarReX):
                    return copy.deepcopy(using[0])
                return StarReX(*using)
            raise Exception("invalid ReX specification")

    def __str__(self):
        if isinstance(self, EmptyReX):
            return "empty"
        if isinstance(self, NilReX):
            return "nil"
        if isinstance(self, SingleReX):
            return self._data[0]
        if isinstance(self, StarReX):
            return f"{str(self._data[0])}*"
        if isinstance(self, CatReX):
            return f"({str(self._data[0])} . {str(self._data[1])})"
        # self is an instance of type AltReX
        return f"({str(self._data[0])} | {str(self._data[1])})"

    def __eq__(self, other):
        if not isinstance(other, ReX):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self._data == other._data

    @property
    def is_nil_aMember(self) -> bool:
        """realises function E: ReX -> bool that determines whether 'self'
        is in the language specified by the function argument"""
        if isinstance(self, EmptyReX) or isinstance(self, SingleReX):
            return False
        elif isinstance(self, NilReX) or isinstance(self, StarReX):
            return True
        elif isinstance(self, CatReX):
            return (self._data[0].is_nil_aMember and self._data[1].is_nil_aMember)
        # self is an instance of AltReX
        return (self._data[0].is_nil_aMember or
                self._data[1].is_nil_aMember)



    def Brzozowski(self, letter: str):
        """'letter' is a string of length one"""
        if not isLetter(letter):
            raise Exception("invalid letter")
        # now compute Brzozowski derivative of the expression
        if (isinstance(self, EmptyReX) or
                isinstance(self, NilReX)):
            return EmptyReX()
        if isinstance(self, SingleReX):
            return NilReX() if self._data[0] == letter else EmptyReX()
        if isinstance(self, StarReX):
            return ReX.create('cat', self._data[0].Brzozowski(letter), self)
        if isinstance(self, CatReX):
            mandatory = ReX.create('cat', self._data[0].Brzozowski(letter), self._data[1])
            return (ReX.create('alt', mandatory, self._data[1].Brzozowski(letter)) if self._data[
                0].is_nil_aMember else mandatory)
        else:  # 'self' is an instance of class AltReX
            return ReX.create('alt', self._data[0].Brzozowski(letter),
                              self._data[1].Brzozowski(letter))

class EmptyReX(ReX):     # синтаксичне правило (1)
    def __init__(self):
        self._data = None


class NilReX(ReX):       # синтаксичне правило (2)
    def __init__(self):
        self._data = ()


class SingleReX(ReX):    # синтаксичне правило (3)
    def __init__(self, letter):
        """'letter' is a string of length one"""
        if not isLetter(letter):
            raise Exception("invalid letter")
        self._data = (letter,)


class StarReX(ReX):      # синтаксичне правило (4)
    def __init__(self, rex: ReX):
        if not isinstance(rex, ReX):
            raise Exception("invalid regular expression")
        self._data = (rex,)


class CatReX(ReX):      # синтаксичне правило (5)
    def __init__(self, rex1: ReX, rex2: ReX):
        if not (all(map(isinstance, (rex1, rex2), (ReX, ReX)))):
            raise Exception("invalid regular expression")
        self._data = (rex1, rex2)


class AltReX(ReX):      # синтаксичне правило (6)
    def __init__(self, rex1: ReX, rex2: ReX):
        if not (all(map(isinstance, (rex1, rex2), (ReX, ReX)))):
            raise Exception("invalid regular expression")
        self._data = (rex1, rex2)


def naive_recognition(rex, word):
    """returns 'True' if the list 'word' of letters represents the word
    belonging to the language specified by the regular expression 'rex'
    """
    if not isinstance(rex, ReX):
        raise Exception("invalid regular expression")
    if not (isinstance(word, list) and
            all(map(isinstance, word, len(word) * [str])) and
            all(map(lambda x: len(x) == 1, word))):
        raise Exception("invalid word")
    # Now, let us recognise
    rex_curr = copy.deepcopy(rex)
    for a in word:
        rex_curr = rex_curr.Brzozowski(a)
    return rex_curr.is_nil_aMember


def isLetter(x):
    return isinstance(x, str) and len(x) == 1

def get_alphabet(rex: ReX) -> list:
    alphabet = []
    list1 = ('*', '.', '(', ')', '|')
    list2 = []
    for i in rex.__str__():
        if i not in list1:
            list2.append(i)
    list2 = ("".join(list2)).split()
    for i in list2:
        if isLetter(i) and i not in alphabet:
            alphabet.append(i)
    return alphabet

class Acceptor:
    def __init__(self, spec):
        self._S = []
        self._data = spec                   # регулярний вираз
        self._alphabet = get_alphabet(spec) #
        self._doDict = dict()               #

    def run(self, state, u):

        if u:
            a, u_new = u[0], u[1:]
            return self.run(self._doDict[state][a], u_new)
        return state

    def isAcceptable(self, u):
        return self._doDict[self.run(0, u)]['acceptant']

    def get_Q(self, rex: ReX):
        rex_cop_list = list()
        for i in self._alphabet:
            rex_cop_list.append(copy.deepcopy(self._data))  # список для поточних станів після диференціювання
        states_rex = [rex]  # список станів типу ReX
        states_rex_str = [rex.__str__()]  # список станів у вигляді рядків
        j = 1
        r_list = len(self._alphabet) * [0]
        for i in range(len(self._alphabet)):  # створюю перші n станів, де n == довжині алфавіту
            r_list[i] = (rex_cop_list[i]).Brzozowski(self._alphabet[i])
            if r_list[i].__str__() not in states_rex_str:  # Якщо новий стан не входить до існуючих - запам'ятовуємо його
                states_rex.append(r_list[i])
                states_rex_str.append(r_list[i].__str__())
        while True:
            for i in range(len(self._alphabet)):  # продовжую диференціювати, поки не отримаю порожній стан
                r_list[i] = states_rex[j].Brzozowski(self._alphabet[i])
                if r_list[i].__str__() not in states_rex_str:
                    states_rex.append(r_list[i])
                    states_rex_str.append(r_list[i].__str__())
            if r_list == states_rex:
                break
            if r_list[-1].__str__() == 'empty':
                break
            j += 1
        return states_rex

    def create_acceptor(self, rex: ReX) -> dict:
        print(f"alphabet = {self._alphabet}")
        internal_keys = copy.deepcopy(self._alphabet)
        internal_keys.append("acceptant")  # список станів словника doDict
        states_rex = self.get_Q(rex)
        states_rex_str = list()
        for i in states_rex:
            states_rex_str.append(i.__str__())
        print(f"states_rex_str: {states_rex_str}")
        l = [int(i) for i in range(len(states_rex))]
        do_dict = dict.fromkeys(l)  # створюю словник, ключами якого є стани (0, ..., n)
        state_dict = dict.fromkeys(states_rex_str)
        for i in l:  # створюю допоміжний словник, ключами якого є str стани, а значеннями (0, ..., n)
            state_dict[states_rex_str[i]] = int(i)
        for state in states_rex:  # заповнення словника do_dict
            internal_dictionary = dict.fromkeys(internal_keys)  # створення вбудованого словника
            for key in internal_keys:  # заповнення значень вбудованого словника
                if key is internal_keys[-1]:
                    internal_dictionary[key] = str(state.is_nil_aMember)
                    break
                internal_dictionary[key] = state_dict[(state.Brzozowski(key)).__str__()]
            do_dict[state_dict[state.__str__()]] = internal_dictionary  # присвоєння значень словнику скінченного акцептора, значеннями якого є вбудовані словники

        for i in do_dict:  # вивід словника
            print(i, ":")
            for j in do_dict[i]:
                print('\t', j, " : ", do_dict[i][j])
        self._doDict = do_dict
        return do_dict


# перший приклад з лекції
rex1 = AltReX(        # створення регулярного виразу
    AltReX(
        NilReX(),
        CatReX(
            CatReX(
                CatReX(
                    SingleReX('a'),
                    StarReX(SingleReX('b'))
                ),
                SingleReX('a')
            ),
            SingleReX('b')
        )
    ),
    CatReX(
        CatReX(
            CatReX(
                SingleReX('b'),
                StarReX(SingleReX('a')),
            ),
            SingleReX('b')
        ),
        SingleReX('a')
    )
)
print('\n', rex1)
A = Acceptor(rex1)
do_dict = A.create_acceptor(rex1)  # створюю словник скінченного акцептора
print(do_dict)
print("run(0, a): ", A.run(0, 'a'))
print(f"A.isAcceptable('abbab'): {A.isAcceptable('abbab')}")  # перевіряю належність слова='abbab' мові, заданим регулярним втразом rex1

# другий приклад
# (a . b)* | c
rex2 = AltReX(
    StarReX(
        CatReX(
            SingleReX('a'),
            SingleReX('b')
        )
    ),
    SingleReX('c')
)
print('\n', rex2)
B = Acceptor(rex2)
do_dict2 = B.create_acceptor(rex2)
print(f"B.isAcceptable('abbab'): {B.isAcceptable('aab')}")  # перевіряю належність слова='aab' мові, заданим регулярним втразом rex2

# (a.b*.a|b)*
rex3 = StarReX(
    AltReX(
        CatReX(
            CatReX(
                SingleReX('a'),
                StarReX(SingleReX('b'))
            ),
            SingleReX('a')
        ),
        SingleReX('b')
    )
)
print('\n', rex3)
C = Acceptor(rex3)
do_dict3 = C.create_acceptor(rex3)
print(f"F.isAcceptable('aabbabbbab'): {C.isAcceptable('aabbabbbab')}")

# (a.b.(b.b)*.a|b)*
rex4 = StarReX(
    AltReX(
        CatReX(
            CatReX(
                SingleReX('a'),
                CatReX(
                    SingleReX('b'),
                    StarReX(CatReX(SingleReX('b'), SingleReX('b')))
                )
            ),
            SingleReX('a')
        ),
        SingleReX('b')
    )
)
print('\n', rex4)
D = Acceptor(rex4)
do_dict4 = D.create_acceptor(rex4)
print(do_dict4)
print(f"F.isAcceptable('aabbabbbab'): {D.isAcceptable('aabbabbbab')}")