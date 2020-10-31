# МОДУЛЬ генерации случайного ключа для AES-128
import random

def get_key():
    key = bytearray()
    for i in range(16):
        key.append(random.getrandbits(8))
    print("KEY from MODULE: {0}".format(key))
    return key


# def write_key()