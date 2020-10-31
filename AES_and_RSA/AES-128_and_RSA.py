# -*- coding: utf-8 -*-
# -- Программа шафрования/дешифрования по алгоритму AES-128 --
from AES_and_RSA import encrypt
from AES_and_RSA import decrypt
from AES_and_RSA import generate_key
from RSA import RSA

# Работа ведется в кодировке UTF-8
# Инициализация некоторых исходных данных
from AES_and_RSA import table_data


# Функция ввода исходных данных. Принимает от пользователя ключ в виде символов кириллицы (для удобства).
def input_data():
    key = ''
    choices_function = int(input("Шифровать/Дешифровать? (1/2): "))
    if choices_function == 1:
        while True:
            # key = input("Введите ключ (кириллицей): ")
            key = generate_key.get_key()
            encript_key = RSA.rsa(from_main=False, _key=key)
            with open('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы'
                      '\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts'
                      '\encrypt_key.txt', 'w', encoding='utf-8-sig') as file:
                for _byte in encript_key:
                    file.write(str(_byte) + '\n')
            break
            # if len(key.encode()) == 16:
            #     key = bytearray(key.encode())
            #     break
            # else:
            #     print("Ключ должен быть длиной 8 символов (16 байт в utf-8)")
    type_input_data = int(input("Данные вводим с клавиатуры или из файла? (1/2): "))
    if type_input_data == 1:
        string = input("Введите текст: ")
    else:
        path_to_file = input(
            "Введите путь (D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы"
            "\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts\encrypt_text.txt): ")
        with open(path_to_file, "r", encoding='utf-8-sig') as file:      # encoding='UTF-8'
            string = file.read()

    if choices_function == 2:
        # Считываение ключа
        new_key = list()
        with open('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы'
                  '\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts'
                  '\encrypt_key.txt', 'r', encoding='utf-8-sig') as file:
            for line in file:
                new_key.append(int(line.strip()))
        print("READ_KEY: {0}".format(new_key))
        key = RSA.rsa_dec(new_key)
        print("DECRYPT_KEY: {0}".format(key))


    # print("Код.стр.: " + str(string))
    # print("Ключ    : " + str(key))
    # choices_function - кодировать или декодировать
    # ley - ключ
    # string - кодируемые байты

    return choices_function, key, string


# Функция парсит последовательность строковых символов в байты
def string_to_hex(string):
    text_bytes = bytearray()
    i = 0
    while i < len(string):
        print("2 символа: {0}".format(string[i+3 : i+5]))
        print("тип символов: {0}".format(type(string[i+3 : i+5])))
        _byte = bytes.fromhex(string[i+3 : i+5])[0]
        print("byte: {0}".format(_byte))
        text_bytes.append(_byte)
        print("text byte: {0}".format(text_bytes))
        i += 5
    print('закодированная: {0}'.format(text_bytes))
    return text_bytes
# \0x14\0xcc\0x26\0xd4\0xfd\0xdc\0xa5\0xca\0x06\0x02\0x09\0xf1\0xa9\0x1d\0x02\0xa6


# Функция нормализует текст, т.е. если не хватает байтов до 16, заполняет символом '('; ord(40) == '('; hex = 0x28
def normalize_text(string):
    if str == type(string):
        array_bytes = bytearray(string.encode(encoding='utf-8'))
    else:
        array_bytes = string
    ost = len(array_bytes) % 16
    if ost != 0:
        for i in range(16-ost):
            array_bytes.append(0x28)
    # print('normalize array_bytes: {0}'.format(array_bytes))
    return array_bytes

# Основная функция
def main():
    choices_function, key, string = input_data()
    # string = bytearray(b'\x00\x04\x12\x14\x12\x04\x12\x00\x0C\x00\x13\x11\x08\x23\x19\x19\x00\x04\x12\x14\x12\x04\x12\x00\x0C\x00\x13\x11\x08\x23\x19\x19')
    print("STRING: {0}, len(STRING) = {1}".format(string, len(string)))
    if choices_function == 1:
        text_bytes = normalize_text(string)
    else:
        text_bytes = string_to_hex(string)
    _round = 0
    output_encrypt_bytes = list()
    output_decrypt_bytes = list()
    # testing bytes from book (страница 241)
    # text_bytes = bytearray(b'\x00\x04\x12\x14\x12\x04\x12\x00\x0C\x00\x13\x11\x08\x23\x19\x19')     # <--- text for encrypt
    # testing encrypt_bytes
    # text_bytes = bytearray(b'\xbc\x02\x8b\xd3\xe0\xe3\xb1\x95\x55\x0d\x6d\xf8\xe6\xf1\x82\x41')     # <--- text for decrypt
    if choices_function == 1:
        # testing keys
        # key = bytearray(b'\x0f\x15\x71\xc9\x47\xd9\xe8\x59\x0c\xb7\xad\xdf\xaf\x7f\x67\x98')
        # key = bytearray(b'\x24\x75\xA2\xB3\x34\x75\x56\x88\x31\xE2\x12\x00\x13\xAA\x54\x87')

        # key for book
        # key = bytearray(b'\x24\x75\xA2\xB3\x34\x75\x56\x88\x31\xE2\x12\x00\x13\xAA\x54\x87')     # <--- key
        print("KEY = {0}".format(key))
        rounds_key = encrypt.expand_key(key)                                # !!!!!!!!!!!!!!!!!!!!!!!!!! расширение ключа
        for key in rounds_key:
            print("key: {0}".format(key))

        # Разбиваем текст на блоки и оперируем ими, но при этом каждая первая итерация над блоком будет проводиться отдельно
        for i in range(int(len(text_bytes)/16)):
            print('---' * 20 + '\n' + 'round: {0}'.format(_round) + '\n' + '---' * 20)
            block = []                                                      # !!!!!!!!!!!!!!!!!!!!!!!!!! блок
            text = text_bytes[i*16 : (i+1)*16]
            for j in range(4):
                block.append(text[j*4 : (j+1)*4])
            state = encrypt.add_round_key(_round, rounds_key, block)        # !!!!!!!!!!!!!!!!!!!!!!!!!! матрица состояний
            _round = 1
            for i in range(1, 10):
                print('---' * 20 + '\n' + 'round: {0}'.format(_round) + '\n' + '---' * 20)
                state = encrypt.sub_bytes(state)                            # !!!!!!!!!!!!!!!!!!!!!!!!!! операция замены байтов
                # print("state после sub_bytes: {0}".format(state))
                print("sub_bytes Выполнилось")
                state = encrypt.shift_rows(state)                           # !!!!!!!!!!!!!!!!!!!!!!!!!! операция циклического сдвига байтов
                print("shift_rows Выполнилось")
                state = encrypt.mix_columns(state)
                print("mix_columns Выполнилось")
                state = encrypt.add_round_key(_round, rounds_key, state)    # !!!!!!!!!!!!!!!!!!!!!!!!!! операция добавления ключа
                print("add_round_key Выполнилось")
                _round += 1
            print('---' * 20 + '\n' + 'round: {0}'.format(_round) + '\n' + '---' * 20)
            state = encrypt.sub_bytes(state)
            state = encrypt.shift_rows(state)
            state = encrypt.add_round_key(_round, rounds_key, state)
            output_encrypt_bytes += state
            _round = 0
        result = bytearray()
        _str_result = ''
        for i in output_encrypt_bytes:
            result += i
            for j in i:
                if len(hex(j)) == 3:
                    _str_result += '\\' + hex(j)[0:2] + '0' + hex(j)[-1]
                else:
                    _str_result += '\\' + hex(j)
        with open('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы'
                  '\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts'
                  '\encrypt_text.txt', 'w', encoding='utf-8-sig') as file:
            file.write(_str_result)

        print('Зашифрованные байты: {0}'.format(result))
        print('Зашифрованные байты _str_: {0}'.format(_str_result))

    else:
        # key = bytearray(b'\x24\x75\xA2\xB3\x34\x75\x56\x88\x31\xE2\x12\x00\x13\xAA\x54\x87')
        rounds_key = decrypt.expand_key(key)
        for key in rounds_key:
            print("key: {0}".format(key))
        # Разбиваем текст на блоки и оперируем ими, но при этом каждая первая итерация над блоком будет проводиться отдельно
        for i in range(int(len(text_bytes)/16)):
            print('---' * 20 + '\n' + 'round: {0}'.format(_round) + '\n' + '---' * 20)
            block = []                                                      # !!!!!!!!!!!!!!!!!!!!!!!!!! блок
            text = text_bytes[i*16 : (i+1)*16]
            for j in range(4):
                block.append(text[j * 4: (j + 1) * 4])
            state = decrypt.add_round_key(_round, rounds_key, block)  # !!!!!!!!!!!!!!!!!!!!!!!!!! матрица состояний
            _round = 1
            for i in range(1, 10):
                print('---' * 20 + '\n' + 'round: {0}'.format(_round) + '\n' + '---' * 20)
                state = decrypt.inv_shift_rows(state)  # !!!!!!!!!!!!!!!!!!!!!!!!!! операция циклического сдвига байтов
                print("shift_rows Выполнилось")
                state = decrypt.inv_sub_bytes(state)  # !!!!!!!!!!!!!!!!!!!!!!!!!! операция замены байтов
                # print("state после sub_bytes: {0}".format(state))
                print("sub_bytes Выполнилось")
                state = decrypt.add_round_key(_round, rounds_key, state)  # !!!!!!!!!!!!!!!!!!!!!!!!!! операция добавления ключа
                print("add_round_key Выполнилось")
                state = decrypt.inv_mix_columns(state)
                print("inv_mix_columns Выполнилось")

                _round += 1
            print('---' * 20 + '\n' + 'round: {0}'.format(_round) + '\n' + '---' * 20)
            state = decrypt.inv_shift_rows(state)
            state = decrypt.inv_sub_bytes(state)
            state = decrypt.add_round_key(_round, rounds_key, state)
            output_decrypt_bytes += state
            _round = 0
        print('---' * 20 + '\n' + '---' * 20)
        result = bytearray()
        for i in output_decrypt_bytes:
            result += i
        while True:
            if result[-1] == 40:
                result.pop()
            else:
                break
        print('Дешифрованные байты: {0}'.format(result.decode()))
        with open('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы'
                  '\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts'
                  '\decrypt_text.txt', 'w', encoding='utf-8-sig') as file:
            file.write(str(result.decode()))
# Точка входа
main()


# key: [bytearray(b'$u\xa2\xb3'), bytearray(b'4uV\x88'), bytearray(b'1\xe2\x12\x00'), bytearray(b'\x13\xaaT\x87')]
# key: [bytearray(b'\x89U\xb5\xce'), bytearray(b'\xbd \xe3F'), bytearray(b'\x8c\xc2\xf1F'), bytearray(b'\x9fh\xa5\xc1')]
# key: [bytearray(b'\xceS\xcd\x15'), bytearray(b'ss.S'), bytearray(b'\xff\xb1\xdf\x15'), bytearray(b'`\xd9z\xd4')]
# key: [bytearray(b'\xff\x89\x85\xc5'), bytearray(b'\x8c\xfa\xab\x96'), bytearray(b'sKt\x83'), bytearray(b'\x13\x92\x0eW')]
# key: [bytearray(b'\xb8"\xde\xb8'), bytearray(b'4\xd8u.'), bytearray(b'G\x93\x01\xad'), bytearray(b'T\x01\x0f\xfa')]
# key: [bytearray(b'\xd4T\xf3\x98'), bytearray(b'\xe0\x8c\x86\xb6'), bytearray(b'\xa7\x1f\x87\x1b'), bytearray(b'\xf3\x1e\x88\xe1')]
# key: [bytearray(b'\x86\x90\x0b\x95'), bytearray(b'f\x1c\x8d#'), bytearray(b'\xc1\x03\n8'), bytearray(b'2\x1d\x82\xd9')]
# key: [bytearray(b'b\x83>\xb6'), bytearray(b'\x04\x9f\xb3\x95'), bytearray(b'\xc5\x9c\xb9\xad'), bytearray(b'\xf7\x81;t')]
# key: [bytearray(b'\xeea\xac\xde'), bytearray(b'\xea\xfe\x1fK'), bytearray(b'/b\xa6\xe6'), bytearray(b'\xd8\xe3\x9d\x92')]
# key: [bytearray(b'\xe4?\xe3\xbf'), bytearray(b'\x0e\xc1\xfc\xf4'), bytearray(b'!\xa3Z\x12'), bytearray(b'\xf9@\xc7\x80')]
# key: [bytearray(b'\xdb\xf9.&'), bytearray(b'\xd58\xd2\xd2'), bytearray(b'\xf4\x9b\x88\xc0'), bytearray(b'\r\xdbO@')]

# Зашифрованные байты bytearray(b'\x14\xcc&\xd4\xfd\xdc\xa5\xca\x06\x02\t\xf1\xa9\x1d\x02\xa6'):
# Зашифрованные байты _str_:  \0x14\0xcc\0x26\0xd4\0xfd\0xdc\0xa5\0xca\0x06\0x02\0x09\0xf1\0xa9\0x1d\0x02\0xa6