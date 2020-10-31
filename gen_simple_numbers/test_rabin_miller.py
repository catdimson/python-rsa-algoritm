# -- Программа реализации алгоритма теста Рабина-Миллера --
import timeit
import random
from random import randrange


def fast_pow(base, degree, module):
    degree = bin(degree)[2:]
    r = 1

    for i in range(len(degree) - 1, -1, -1):
        r = (r * base ** int(degree[i])) % module
        base = (base ** 2) % module
    return r


# def test_Rabin_Miller(n, k):
#     if n == 2 or n == 3:
#         return True
#     if n < 2 or n % 2 == 0:
#         return False
#
#     d = n - 1
#     s = 0
#     while d % 2 == 0:
#         d //= 2
#         s += 1
#     # print('d = {0}'.format(d))
#     # print('s = {0}'.format(s))
#     # print('---'*20)
#
#     for i in range(k):
#         a = random.randint(2, n - 2)
#         x = fast_pow(a, d, n)
#         # print('a = {0}'.format(a))
#         # print('x = {0}'.format(x))
#
#         if x == 1 or x == n - 1:
#             continue
#
#         for j in range(1, s):
#             x = fast_pow(x, 2, n)
#             # print('x = {0}'.format(x))
#
#             if x == 1:
#                 return False
#             if x == n - 1:
#                 return True
#         return False
#     return True


def test_Rabin_Miller(n, k=10):
    if n == 2:
        return True
    if not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


if __name__ == '__main__':
    n = int(input("n = "))
    k = 10
    res = test_Rabin_Miller(n, k)
    if res == True:
        print("Вероятно простое")
    else:
        print("Составное")