from cryptography_library.DES import DES
from cryptography_library.playfair import playfair_decrypt, playfair_encrypt
from cryptography_library.vigenere import vigenere_decry, vigenere_encry
from cryptography_library.column_permutation_cipher import column_decry, column_encry
from cryptography_library.double_transposition import double_decry, double_encry
from cryptography_library.autokey import autokey_cipher_encrypt
from cryptography_library.autokey import autokey_cipher_decrypt
from cryptography_library.RC4 import RC4_encrypt
from cryptography_library.RC4 import RC4_decrypt
from cryptography_library.playfair import playfair_encrypt, playfair_decrypt
from cryptography_library.rsa import rsa_encrypt, rsa_decrypt
from cryptography_library.MD5 import md5
from cryptography_library.dh_key_exchange import DHKeyExchange


def caesar_cipher_encrypt(plain_text: str, key: str):  

    """
    :param plain_text: 明文
    :param key: 密钥
    :return:加密密文
    """
    # 字符表
    mstr = 'abcdefghijklmnopqrstuvwxyz'
    # 字符表长度
    lengthM = len(mstr)

    cipher_text = ''
    for x in plain_text:
        if x in mstr:
            numX = mstr.index(x)  # 获取x字符在mstr中的位置
            # 新的字符位置加上key
            keys = int(key)
            numX = (numX + keys) % lengthM
            cipher_text = cipher_text + mstr[numX]
    return cipher_text


def caesar_cipher_decrypt(cipher_text: str, key: str):  
    """

    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """
    # 字符表
    mstr = 'abcdefghijklmnopqrstuvwxyz'
    # 字符表长度
    lengthM = len(mstr)
    plain_text = ''
    for x in cipher_text:
        if x in mstr:
            # 获取x字符在mstr中的位置
            numX = mstr.index(x)
            # 新的字符位置加上key
            keys = int(key)
            numX = (numX - keys) % lengthM
            plain_text = plain_text + mstr[numX]

    return plain_text


def keyword_cipher_encrypt(plain_text: str, key: str):
    s1 = ""
    for i in key:
        if i not in s1:
            s1 += i
    s2 = ""
    s3 = "abcdefghijklmnopqrstuvwxyz"
    for i1 in s3:
        if i1 not in s1:
            s2 += i1
    keys = s1 + s2
    cipher_text = ""
    plain_text = plain_text.lower()
    for i2 in plain_text:
        numI = s3.index(i2)
        cipher_text = cipher_text + keys[numI]
    return cipher_text


def keyword_cipher_decrypt(cipher_text: str, key: str):
    s1 = ""
    for i in key:
        if i not in s1:
            s1 += i
    s2 = ""
    s3 = "abcdefghijklmnopqrstuvwxyz"
    for i1 in s3:
        if i1 not in s1:
            s2 += i1
    keys = s1 + s2
    plain_text = ""
    cipher_text = cipher_text.lower()
    for i2 in cipher_text:
        numI = keys.index(i2)
        plain_text = plain_text + s3[numI]
    return plain_text


def play_fair_encrypt(plain_text: str, key: str) -> str: 
    """

    :param plain_text: 明文
    :param key: 密钥
    :return:加密密文
    """
    return playfair_encrypt(plain_text, key)


def play_fair_decrypt(cipher_text: str, key: str) -> str:  
    """

    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """
    return playfair_decrypt(cipher_text, key)


def autokey_plain_text_encrypt(plain_text: str, key: str):  
    """

    :param plain_text: 明文，均为字母字符，非字母字符的均会在函数中被删去
    :param key: 密钥，均为字母字符，非字母字符的均会在函数中被删去
    :return:加密密文，均为小写字母
    """
    return autokey_cipher_encrypt(plain_text, key)


def autokey_plain_text_decrypt(cipher_text: str, key: str): 
    """

    :param cipher_text: 密文，均为字母字符，非字母字符的均会在函数中被删去
    :param key: 密钥，均为字母字符，非字母字符的均会在函数中被删去
    :return: 明文，均为小写字母
    """
    return autokey_cipher_decrypt(cipher_text, key)


def DES_encrypt(plain_text: str, key: str, file=False) -> str:  
    """

    :param file: if it is a file
    :param plain_text: 明文, (if it's a file ,the plain_text could be bytes)
    :param key: 密钥
    :return:加密密文
    """
    my_hexdata = key
    scale = 16
    num_of_bits = 8
    # print("my_hex_data", my_hexdata)
    key_bin = bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
    des = DES()

    if not file:
        plain_text = plain_text.encode("utf-8")
    return des.encrypt_file(plain_text, key_bin)


def DES_decrypt(cipher_text: str, key: str, file=False) -> str: 
    """

    :param file: if it is a file
    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """
    my_hexdata = key
    scale = 16
    num_of_bits = 8
    key_bin = bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
    des = DES()
    if file:
        return des.decrypt_file(cipher_text, des.short_key_to_long(key))
    return des.decrypt_file(cipher_text, key_bin).decode('utf-8')


def vigenere_encrypt(plain_text: str, key: str) -> str:  
    """

    :param plain_text: 明文
    :param key: 密钥
    :return:加密密文
    """
    return vigenere_encry(plain_text, key)


def vigenere_decrypt(cipher_text: str, key: str) -> str: 
    """

    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """
    return vigenere_decry(cipher_text, key)


def coloumn_permutation_encrypt(plain_text: str, key: str) -> str:  # 吕泽宇
    """

    :param plain_text: 明文
    :param key: 密钥
    :return:加密密文
    """
    return column_encry(plain_text, key)


def coloumn_permutation_decrypt(cipher_text: str, key: str) -> str: 
    """

    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """
    return column_decry(cipher_text, key)


def double_transposition_encrypt(plain_text: str, key: str) -> str:  
    """

    :param plain_text: 明文
    :param key: 密钥
    :return:加密密文
    """
    return double_encry(plain_text, key)


def double_transposition_decrypt(cipher_text: str, key: str) -> str: 
    """

    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """
    return double_decry(cipher_text, key)


def RC4_cipher_encrypt(plaintext: str, key: str):  
    """

        :param plaintext: 待加密的明文字符串
        :param key: RC4加密使用的密钥，字符串
        :return:
    """

    return RC4_encrypt(plaintext, key)


def RC4_cipher_decrypt(ciphertext: str, key: str):  
    """

        :param ciphertext: 用RC4加密的密文字符串
        :param key: RC4加密使用的密钥，字符串
        :return:
    """

    return RC4_decrypt(ciphertext, key)


def RSA_cipher_encrypt(ciphertext: str, key: str):
    """
    :param ciphertext: 明文
    :param key: 公钥
    :return:
    """
    key_t = eval(key)
    return rsa_encrypt(ciphertext, key_t)


def RSA_cipher_decrpt(plaintext: str, key: str):
    """

    :param ciphertext:
    :param key:
    :return:
    """
    key_t = eval(key)
    return rsa_decrypt(plaintext, key_t)


def MD5(text: str):
    """

    :param text: 需要计算数字签名的字符串
    :return:
    """
    return md5(text)


def DH_exchange_demo():
    a = DHKeyExchange()
    b = DHKeyExchange()
    pa = a.get_public_one()
    pb = b.get_public_one()
    c = a.get_shared_key(pb)
    d = b.get_shared_key(pa)
    text = "key from A:\n" + str(pa) + '\n key from B:\n' + str(pb) + "\nShared key from a:\n" + str(
        c) + "\nShared key form b:\n" + str(d)

    return text



