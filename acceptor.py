def accept(str):
    flag, dot, e = True, False, False
    if str == "inf" or str == "nan":
        return True
    for i in range(len(str)):
        if str[i].isdigit():         # стан цифри
            flag = True
        elif str[i] == '.':          # стан точки
            if dot is False:         # якщо це перша точка
                flag, dot = True, True
            else:
                return False
        elif str[i] in ['-', '+']:   # стан знаку
            if i == len(str)-1:      # якщо знак є останнім символом
                return False
            elif str[i-1].lower() == 'e' and str[i+1].isdigit():  # знак і цифри експоненти
                flag = True
            elif i == 0:             # якщо знак є першим символом
                flag = True
            else:
                return False
        elif str[i].lower() == 'e':  # стан для експоненти
            if dot is True and e is False:
                flag, e = True, True
            else:
                return False
        else:
            return False
    return True if flag is True and str[-1].lower() != 'e' else False


def acceptCheck(num):  # Функція для перевірки правильності работи акцептора
    try:
        float(num)
        return True
    except ValueError:
        return False

A = ["23.05", "-34.2e-3", "1.6e", "7.2e-3e-2", "1.6e7", "1.4e-", "inf", "nan"]  # послідовність вхідних значень

print("accept:      " + ", ".join([str(accept(a)) for a in A]))
print("acceptCheck: " + ", ".join([str(acceptCheck(a)) for a in A]))


