# -*- coding: utf-8 -*-
#  -- Модуль дешифрования байтов --
from table_data import InvSBox, SBox
import operator
indexes = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15
}
mix_matrix = [
    bytearray(b'\x0E\x0B\x0D\x09'),
    bytearray(b'\x09\x0E\x0B\x0D'),
    bytearray(b'\x0D\x09\x0E\x0B'),
    bytearray(b'\x0B\x0D\x09\x0E')
]


# --/ НЕ Протестирована /
# Фунция расширения ключа.
def expand_key(key):                        # аргумент key - строка из 16 байт ('a2b3c4') к примеру
    # генерируем пустой список, где будут храниться раундовые ключи
    # key = bytearray(key.encode())
    rounds_key = []
    for i in range(11):
        rounds_key.append([''] * 4)
    for i in range(4):      # записываем первичный ключ key в список _key первым (под индексом _key[0])
        rounds_key[0][i] = key[i*4 : (i+1)*4]
    # for el in rounds_key:
    #     print(el)
    # print('---'*20 + '\n' + '---'*20)

    # Константы R_const
    R_con = bytearray()
    R_con = (b'\x01\x02\x04\x08\x10\x20\x40\x80\x1b\x36')

    # Функция добавления первого слова раунда в rounds_key
    def add_first_word(_round, rounds_key):               # first_word - аргумент, хранящие первые 4 байта ключа
        last_prev_word = rounds_key[_round-1][3].copy()
        first_prev_key = rounds_key[_round-1][0].copy()
        # print(first_prev_key)
        # print(last_prev_word)
        # Шаг 1. циклический сдвиг четырехбайтового слова влево на один байт
        last_prev_word.append(last_prev_word[0])
        del last_prev_word[0]
        # print("После шага 1: " + str(last_prev_word))
        # Шаг 2. замена каждого байта слова, полученного на шаге 1, в соответствии с таблицей SubBytes , используемой при шифровании (операция SubWord)
        for i in range(4):
            # Костыль
            _byte = bytes([last_prev_word[i]]).hex()           # Байт в типе - строка. Индекс 0 - первый знак (номер строки SBox), индекс 1 - второй знак (номер столбца): byte[4] и byte[5]
            # print(_byte)        # _byte - <class 'str'>
            last_prev_word[i] = SBox[ indexes[_byte[0]] ][ indexes[_byte[1]] ]
        # print("После шага 2: " + str(last_prev_word))
        # Шаг 3. суммирование по mod 2 байтов, полученных на шаге 2, с раундовой постоянной
        last_prev_word[0] = operator.xor(R_con[_round-1], last_prev_word[0])
        # print("После шага 3: " + str(last_prev_word))

        # Смотреть в формулы
        first_current_word = bytearray()
        # xor по модулю 2 last_prev_word и first_prev_key
        # print("round: {0}".format(_round))
        for i in range(4):
            first_current_word.append( operator.xor(last_prev_word[i], first_prev_key[i]) )
        rounds_key[_round][0] = first_current_word

    # Функция получения слов раунда, кроме первого
    def add_words_round(_round, rounds_key):
        for i in range(1, 4):
            prev_word = rounds_key[_round-1][i].copy()
            current_round_prev_word = rounds_key[_round][i-1].copy()

            # print(prev_word)
            # print(current_round_prev_word)

            current_word = bytearray()
            for j in range(4):
                # print('j: {0}'.format(j))
                current_word.append( operator.xor(prev_word[j],current_round_prev_word[j]) )
            rounds_key[_round][i] = current_word

    # Генерация всех ключей
    for i in range(1, 11):
        add_first_word(i, rounds_key)

        # print("---" * 20)
        # for el in rounds_key:
        #     print(el)
        # print("---" * 20)

        add_words_round(i, rounds_key)
    # for el in rounds_key:
    #     print(el)
    rounds_key.reverse()

    return rounds_key


# --/ НЕ Протестирована /
# Операция XOR над ключём раунда и матрицей состояний
def add_round_key(_round, rounds_key, block):       # На всех этапе кроме первого вместо block передается state
    state = []
    for i in range(4):
        state.append(bytearray(4))
    key_matrix = rounds_key[_round]
    print('state: {0}'.format(state))
    print('key_matrix: {0}'.format(key_matrix))
    print('block: {0}'.format(block))
    for i in range(4):
        for j in range(4):
            state[i][j] = operator.xor( key_matrix[i][j], block[i][j] )
    print('new_state: {0}'.format(state))

    return state


# --/ НЕ Протестирована /
# Функция циклического сдвига строк матрицы состояний на различные значения
def inv_shift_rows(state):
    transform_matrix = []                   # меняем столбцы на строки, чтобы легче было производить операции
    for i in range(4):
        transform_matrix.append(bytearray(4))
    # print("---" * 20 + '\n' + "---" * 20 + '\n' + "---" * 20)
    # print("state:")
    # for el in state:
    #     print(el)
    # print("---" * 20 + '\n' + "---" * 20 + '\n' + "---" * 20)

    for i in range(4):
        for j in range(4):
            transform_matrix[j][i] = state[i][j]
    # print("transform_matrix:")
    # for el in transform_matrix:
    #     print(el)
    # print("---" * 20 + '\n' + "---" * 20 + '\n' + "---" * 20)

    for i in range(4):                       # циклический сдвиг в трансформированной матрице
        for j in range(i):
            shift_byte = transform_matrix[i][-1]
            transform_matrix[i].insert(0, shift_byte)
            del transform_matrix[i][-1]
    # print("transform_matrix_after_shift:")
    # for el in transform_matrix:
    #     print(el)
    # print("---" * 20 + '\n' + "---" * 20 + '\n' + "---" * 20)

    for i in range(4):
        for j in range(4):
            state[i][j] = transform_matrix[j][i]
    # print("state_after_shift:")
    # for el in state:
    #     print(el)
    # print("---" * 20 + '\n' + "---" * 20 + '\n' + "---" * 20)
    del transform_matrix
    return state


# --/ НЕ Протестирована /
# Функция замены байтов
def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            _byte = bytes([state[i][j]]).hex()
            # print("_byte: {0}".format(_byte))
            state[i][j] = InvSBox[indexes[_byte[0]]][indexes[_byte[1]]]
            # print("state[i][j]: {0}".format(state[i][j]))
    return state


# --/ НЕ Протестирована /
# Функция смешивания данных внутри каждого столбца матрицы состояния
def inv_mix_columns(state):
    print("state: {0}".format(state))
    state = state.copy()
    # Для умножение на 02
    def mul_02(num):
        if num < 0x80:
            res = (num << 1)
        else:
            res = (num << 1) ^ 0x1b
        return res % 0x100

    # Для умножение на 02
    def mul_03(num):
        return (mul_02(num) ^ num)

    # Для умножение на 09
    def mul_09(num):
        # return mul_by_03(num)^mul_by_03(num)^mul_by_03(num) - works wrong, I don't know why
        return mul_02(mul_02(mul_02(num))) ^ num

    # Для умножение на 0b
    def mul_0b(num):
        # return mul_by_09(num)^mul_by_02(num)
        return mul_02(mul_02(mul_02(num))) ^ mul_02(num) ^ num

    # Для умножение на 0d
    def mul_0d(num):
        # return mul_by_0b(num)^mul_by_02(num)
        return mul_02(mul_02(mul_02(num))) ^ mul_02(mul_02(num)) ^ num

    # Для умножение на 0e
    def mul_0e(num):
        # return mul_by_0d(num)^num
        return mul_02(mul_02(mul_02(num))) ^ mul_02(mul_02(num)) ^ mul_02(num)

    # Для умножения
    def mul_values(num1, num2):
        if num2 == 0x09:
            result = mul_09(num1)
        elif num2 == 0x0b:
            result = mul_0b(num1)
        elif num2 == 0x0d:
            result = mul_0d(num1)
        elif num2 == 0x0e:
            result = mul_0e(num1)
        else:
            result = num1
        return result

    temporary_col = bytearray(4)                # временнная колонка
    for i in range(4):                          # счетчик для колонок
        for j in range(4):                      # счётчик для значений колонки
            middle_value = bytearray()
            for k in range(4):
                middle_value.append(mul_values(state[i][k], mix_matrix[j][k]))
            _itog_byte = 0
            for iter in range(4):
                _itog_byte = operator.xor(_itog_byte, middle_value[iter])
            temporary_col[j] = _itog_byte
        state[i] = temporary_col
        temporary_col = bytearray(4)
    return state