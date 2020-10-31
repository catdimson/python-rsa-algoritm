# -- МОДУЛЬ генерации простого числа --
import random
from random import randrange
simple_numbers = [
    2,	3,	5,	7,	11,	13,	17,	19,	23,	29,	31,	37,	41,	43,	47,	53,	59,	61,	67,	71,
    73,	79,	83,	89,	97,	101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521
]


# def fast_pow(base, degree, module):
#     degree = bin(degree)[2:]
#     r = 1
#
#     for i in range(len(degree) - 1, -1, -1):
#         r = (r * base ** int(degree[i])) % module
#         base = (base ** 2) % module
#     return r
def fast_pow(b,d,m):
    return pow(b,d,m)


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
#
#     for i in range(k):
#         a = random.randint(2, n - 2)
#         x = fast_pow(a, d, n)
#
#         if x == 1 or x == n - 1:
#             continue
#
#         for j in range(1, s):
#             x = fast_pow(x, 2, n)
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


def generate_number(n):
    number = list()
    number.append('1')
    for i in range(n-2):
        number.append(str(random.randint(0, 1)))
    number.append('1')
    number = int('0b' + ''.join(number), 2)
    return number


def generate_simple_number(n):
    # flag_next = False
    while True:
        num = generate_number(n)         # генерируем n-битное число
        # print("num: {0}".format(num))
        # num = num | 1                       # устанавливаем крайний бит в 1, чтобы число стало нечетным
        # if num in simple_numbers:
        #     return num
        #
        # for el in simple_numbers:
        #     if num % el == 0:
        #         flag_next = True
        #         break
        # if flag_next == True:
        #     flag_next = False

        result = test_Rabin_Miller(num, k=10)
        if result == True:
            return num


def gen_sp(n):
    num = generate_simple_number(n)
    return num