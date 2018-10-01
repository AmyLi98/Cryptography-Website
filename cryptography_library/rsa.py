import random
from random import randint
import math


def pseudoprime_number():
    list = []
    list.append(1)  # 最高位定为1
    for i in range(25):
        c = randint(0, 1)
        list.append(c)
    list.append(1)
    ls2 = [str(j) for j in list]
    ls3 = ''.join(ls2)
    d = int(ls3, 2)
    return d


def xn_mod_p2(x, n, p):
    res = 1
    n_int = int(n)
    n_bin = bin(n_int)[2:]
    for i in range(0, len(n_bin)):
        res = res ** 2 % p
        if n_bin[i] == '1':
            res = res * x % p
    return res


def miller_rabin_witness(a, p):
    if p == 1:
        return False
    if p == 2:
        return True
    n = p - 1
    t = int(math.floor(math.log(n, 2)))
    u = 1
    while t > 0:
        u = n / 2 ** t
        if n % 2 ** t == 0 and u % 2 == 1:
            break
        t = t - 1
    b1 = xn_mod_p2(a, u, p)
    for i in range(1, t + 1):
        b2 = b1 ** 2 % p
        if b2 == 1 and b1 != 1 and b1 != (p - 1):
            return False
        b1 = b2
    if b1 != 1:
        return False
    return True


def prime_test_miller_rabin(p, k):
    while k > 0:
        a = randint(2, p - 1)
        if not miller_rabin_witness(a, p):
            return False
        k = k - 1
    return True


def create_prime_number():
    p1 = pseudoprime_number()
    flag = True
    while flag:
        if prime_test_miller_rabin(p1, 10):
            flag = False
        else:
            p1 = p1 + 2
    return p1


def rapid_exp(m: int, e: int, p: int):
    """
    快速指数算法实现，
    :param a:
    :param b:
    :return: a^b mod m
    """
    n = 1
    while e != 0:
        if e % 2 == 1:
            n = m * n % p
            e = e - 1
        else:
            m = m * m % p
            e = e / 2
    return n


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def get_blockbit(n):
    s = 1
    flag = True
    while flag:
        d = 2 ** s
        if d > n:
            return s - 1
            flag = False
        else:
            s = s + 1


def create_rsa_key():
    """
    生成 rsa密钥 和 分组时每组bit
    :return: 请写明返回顺序
    """
    p = create_prime_number()
    q = create_prime_number()
    n = p * q
    qn = (p - 1) * (q - 1)
    flag = True
    while flag:
        d = randint(3, qn)
        if gcd(d, qn) == 1:
            flag = False
    e = findModInverse(d, qn)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def test_key(public_key, private_key):
    if rsa_decrypt(rsa_encrypt("abcdeedfqfwqwefqwtfqrtygwrtheryjnetujketf", public_key), private_key) == "abcdeedfqfwqwefqwtfqrtygwrtheryjnetujketf":
        return True
    else:
        return False


def return_key():
    flag = True
    while flag:
        public_key, private_key = create_rsa_key()
        if test_key(public_key, private_key):
            flag = False
    public_key, private_key = create_rsa_key()
    with open("./rsa_public_key.txt", "w") as f:
        f.write(str(public_key))
    with open("./rsa_private_key.txt", "w") as f:
        f.write(str(private_key))
    return public_key, private_key


def alphabet_to_number(list_plain_text):
    list_number = []
    for i in range(0, len(list_plain_text)):
        a = ord(list_plain_text[i])
        a_bin = bin(a)[2:]
        list_number.append(0)
        for j in range(0, 7):
            list_number.append(ord(a_bin[j]) - ord('0'))
    return list_number


def number_into_block(list_number, blockbit):
    list_number_blocked = []
    list1 = []
    for i in range(0, len(list_number), blockbit):
        list1.append(list_number[i:i + blockbit])
    zeronum = blockbit - len(list1[len(list1) - 1])
    while len(list1[len(list1)-1]) < blockbit:
        list1[len(list1)-1].append(0)
    for i in range(0, len(list1)):
        a = 0
        for j in range(0, len(list1[i])):
            a = a + 2 ** (blockbit - 1 - j) * list1[i][j]
        list_number_blocked.append(a)
    return list_number_blocked, zeronum


def rsa_encrypt(plain_text: str, public_key):
    list_number = []
    plain_text = plain_text.replace(" ", "").replace(",", "")  # 去掉空格和逗号
    # list_plain_text = list(plain_text)  # 字符串转化成列表
    list_plain = plain_text.encode("utf-8")
    list_number_st = bin(int.from_bytes(list_plain, byteorder="big"))[2:]
    list_number_str = list("0" + list_number_st)
    for i in range(len(list_number_str)):
        list_number.append(ord(list_number_str[i])-ord("0"))
    blockbit = get_blockbit(public_key[1])
    e = public_key[0]
    n = public_key[1]
    # list_number = alphabet_to_number(list_plain_text)  # 把字母转化成数字
    list_number_blocked, zero_num = number_into_block(list_number, blockbit)  # 把数字分组
    list_cipher_text = []
    for i in range(0, len(list_number_blocked)):  # 加密
        list_cipher_text.append(rapid_exp(list_number_blocked[i], e, n))
    cipher_text = str(list_cipher_text)
    cipher_text = str(zero_num) + cipher_text
    return cipher_text


def fillzeroI(list_plain_text_bin, blockbit):
    for i in range(0, len(list_plain_text_bin)):
        while len(list_plain_text_bin[i]) < blockbit:
            list_plain_text_bin[i] = "0" + list_plain_text_bin[i]
    return list_plain_text_bin


def rsa_decrypt(cipher_text: str, secrect_key: tuple):
    i = 1
    zeronum = cipher_text[0]
    while cipher_text[i] != "[":
        zeronum = zeronum + cipher_text[i]
        i = i + 1
    zero_num = int(zeronum)
    list_cipher_text = eval(cipher_text[i:])
    list_plain_text = []
    list_plain_text_bin = []
    # plain_text_bin_group = []
    # plain_text = []
    # plain_text1 = []
    for i in range(0, len(list_cipher_text)):
        list_plain_text.append(rapid_exp(list_cipher_text[i], secrect_key[0], secrect_key[1]))
    for i in range(0, len(list_plain_text)):
        list_plain_text_bin.append(bin(list_plain_text[i])[2:])
    blockbit = get_blockbit(secrect_key[1])
    list_plain_text_bin_fill = fillzeroI(list_plain_text_bin, blockbit)
    plain_text_bin = "".join(list_plain_text_bin_fill)
    plain_text_bin = "0b" + plain_text_bin
    ddd = int(int(plain_text_bin[:-zero_num], 2)).to_bytes(len(plain_text_bin[:-zero_num]) // 8, byteorder="big")
    plaintext = ddd.decode("utf-8")
    # for i in range(0, len(plain_text_bin), 8):
    #     if plain_text_bin[i:i + 8] == "00000000":
    #         break
    #     else:
    #         plain_text_bin_group.append(plain_text_bin[i:i + 8])
    # for i in range(0, len(plain_text_bin_group)):
    #     ls2 = [str(j) for j in plain_text_bin_group[i]]
    #     ls3 = ''.join(ls2)
    #     plain_text.append(chr(int(ls3, 2)))
    # for i in range(0, len(plain_text)):
    #     if plain_text[i] != "\x00":
    #         plain_text1.append(plain_text[i])
    # plaintext = "".join(plain_text1)
    return plaintext


# if __name__ == '__main__':
#     aa, bb = return_key()
#     abc = rsa_encrypt("DCfq,,aefq51695dfeq a5啊额地方安措  费啊额发错VSVWSRV", aa)
#     adc = rsa_decrypt(abc, bb)
#     print(adc)
