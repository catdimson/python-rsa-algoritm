# -- Программа реализации алгоритма шифрования RSA --
from gen_simple_numbers import gen_sp, test_rabin_miller, gcd
import math


# Функция получение p и q
def get_p_and_q():
    choice = int(input("p и q генерируем программно или задаём из файла? (1/2): "))
    if choice == 1:

        # Программная генерация
        # получаем p
        n = int(input("Скольки битное число {0} должно быть сгенерировано?: ".format('p')))
        p = gen_sp.gen_sp(n)
        # получаем q
        n = int(input("Скольки битное число {0} должно быть сгенерировано?: ".format('q')))
        while True:
            q = gen_sp.gen_sp(n)
            if q == p:
                continue
            break

        # Ручной ввод
        #     p = int(input("p = "))
        #     if test_rabin_miller.test_Rabin_Miller(p, 10) != True:
        #         print("Число p должно быть простым. ")
        #         continue
        #     else:
        #         break
        # while True:
        #     q = int(input("q = "))
        #     if test_rabin_miller.test_Rabin_Miller(q, 10) != True:
        #         print("Число q должно быть простым. ")
        #         continue
        #     else:
        #         break

        # Задание из файла из файла
    else:
        p, q = '', ''
        path_to_file = input("Введите путь к 'p' (D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы\Лабораторная работа №6 _\Лабораторная работа №6\\RSA\\texts\p.txt): ")
        with open(path_to_file) as file:
            for line in file:
                p += line.strip()
        while True:
            if test_rabin_miller.test_Rabin_Miller(int('0b' + p, 2) ,10) != True:
                p = bin(int(input("Число p должно быть простым. Поробуйте заново. p = ")))[2:]
                continue
            else:
                p = int('0b' + p, 2)
                break
        path_to_file = input("Введите путь к 'q' (D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы\Лабораторная работа №6 _\Лабораторная работа №6\\RSA\\texts\q.txt): ")
        with open(path_to_file) as file:
            for line in file:
                q += line.strip()
        while True:
            if test_rabin_miller.test_Rabin_Miller(int('0b' + q, 2), 10) != True:
                q = bin(int(input("Число q должно быть простым. Поробуйте заново. q = ")))[2:]
                continue
            else:
                q = int('0b' + q, 2)
                break
    return p, q


# Функция получения n
def get_n(p, q):
    return p * q


# Фукнкция получения функции Эйлера
def get_function_Eiler(p, q):
    return (p-1) * (q-1)


# Функция получения открытой экспоненты
def get_e(f_n, start=14):
    for e in range(start, f_n):
        NOD = math.gcd(f_n, e)
        if NOD == 1:
            return e


# Функция получения d. d - это такое число, мультипликативно обратное к числу e по модулю f_n
def get_d(f_n, e):
    res = gcd.gcd(f_n, e)
    # d = f_n - math.fabs(res[2])
    print('res РАВНО: {0}'.format(res))
    if res[2] < 0:
        d = res[2] % f_n # % f_n
    else:
        d = res[2]
    print('d РАВНО: {0}'.format(d))
    return int(d)
    # while True:
        # for k in range(f_n):
        #     d = (k * f_n + 1) / e
        #
        #     if d % 1 == 0:
        #         return int(d), e
        # for i in range(e, f_n):
        #     e += 1
        #     NOD = math.gcd(f_n, e)
        #     if NOD == 1:
        #         break



# Функция записи в файл
def write_in_file(path, key):
    with open(path, 'w', encoding='utf-8-sig') as file:
        for path_key in key:
            file.write(str(path_key) + '\n')

# Version 1
# Функция быстрого возведения в степень по модулю
# def fast_pow(base, degree, module):
#     degree = bin(degree)[2:]
#     r = 1
#
#     for i in range(len(degree) - 1, -1, -1):
#         r = (r * base ** int(degree[i])) % module
#         base = (base ** 2) % module
#     return r

# Version 2
# def fast_pow(a, n, m):
#     res = 1
#     p = a % m
#     while n:
#         if (n & 1):
#             res = (res * p) % m
#         n >>= 1
#         p = (p * p) % m
#     return res

# Version 3
def fast_pow(a,n,m):
    return pow(a,n,m)

# Шифрование (c = m^e mod n)
def rsa_encrypt(m, e, n):
    return fast_pow(m, e, n)
# Дешифрование (m = c^d mod n)
def rse_decrypt(c, d, n):
    return fast_pow(c, d, n)


# Точка входа в программу
def rsa(from_main=True, _key=bytearray()):
    p, q = get_p_and_q()
    print("p = {0}, q = {1}".format(p, q))
    n = get_n(p, q)
    print("n = {0}".format(n))
    f_n = get_function_Eiler(p, q)
    # del p, q
    print("f(n) = {0}".format(f_n))
    e = get_e(f_n)
    # d, e = get_d(f_n, e)
    d = get_d(f_n, e)
    print("d = {0}, e = {1}".format(d, e))

    open_key = (n, e)
    secret_key = (n, d)
    # del p,q,e

    if from_main == True:
        write_in_file('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы\Лабораторная работа №6 _\Лабораторная работа №6\\RSA\\texts\open_key.txt', open_key)
        write_in_file('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы\Лабораторная работа №6 _\Лабораторная работа №6\\RSA\\texts\secret_key.txt', secret_key)
    else:
        write_in_file('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts\open_key.txt', open_key)
        write_in_file('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts\secret_key.txt', secret_key)
        # c = m^e mod n
        encrypt_key = []
        for _byte in _key:
            print("КЛЮЧИ: {0}".format(_key))
            print("ТЕКУЩИЙ КЛЮЧ: {0}".format(_byte))
            encrypt_key.append(rsa_encrypt(_byte, e, n))
            print("E: {0}".format(e))
            print("N: {0}".format(n))
            # print(encrypt_key)
        print("ENCRYPT KEY: {0}".format(encrypt_key))
        return encrypt_key


# Дешифрование ключа
def rsa_dec(_key):
    key, numbers = bytearray(), []
    with open('D:\Учёба\8 семестр (-)\(-) Информационная безопасность\Лабораторные работы'
              '\Лабораторная работа №6 _\Лабораторная работа №6\\AES_and_RSA\\texts'
              '\secret_key.txt', 'r', encoding='utf-8-sig') as file:
        for line in file:
            numbers.append(int(line.strip()))
    n, d = numbers[0], numbers[1]
    for num in _key:
        print("Зашифрованное число: {0}".format(num))
        print("SECRET KEY 1(n)    : {0}".format(numbers[0]))
        print("SECRET KEY 2(d)    : {0}".format(numbers[1]))
        # print("RSE_DECRYPT: {0}".format(rse_decrypt(num, d, n)) )
        res = rse_decrypt(num, d, n)
        key.append(res)
    return key

# При вызове модуля, как основной программы, выполнить следующее:
if __name__ == "__main__":
    rsa()