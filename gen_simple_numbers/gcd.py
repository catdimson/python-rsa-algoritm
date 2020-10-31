# МОДУЛЬ вычисления НОД по расширенному алгоритму Евклида

def gcd(a, b):
    '''An implementation of extended Euclidean algorithm.
    Returns integer x, y and gcd(a, b) for Bezout equation:
        ax + by = gcd(a, b).
    '''
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - x1*q
        y0, y1 = y1, y0 - y1*q
    return (a, x0, y0)
    # return a

# def gcd(a, b):
#     '''A recursive implementation of extended Euclidean algorithm.
#     Returns integer x, y and gcd(a, b) for Bezout equation:
#         ax + by = gcd(a, b).
#     '''
#     if not b:
#         return (1, 0, a)
#     y, x, g = gcd(b, a%b)
#     return (g, x, y - (a // b) * x)