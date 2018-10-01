def get_plain_file():
    """
    获取需要加密的文件
    :return: string
    """
    with open("./plain.txt", "r") as f:
        plain_text = f.read()
    return plain_text


def delete_useless_cha(plain_text):
    """
    删除读取字符串中非英文字母的字符
    :param plain_text:
    :return:
    """
    text_processed = ""
    for i in plain_text:
        if (ord(i) >= 65 and ord(i) <= 90) or (ord(i) <= 122 and ord(i) >= 97):
            text_processed += i
    return text_processed


def convert_to_lower_case(plain_text):
    """
    把字符中大写字母转换成小写字母
    :param plain_text:
    :return:
    """
    text_processed = ""
    for i in plain_text:
        if ord(i) >= 65 and ord(i) <= 90:
            text_processed += chr(ord(i) + 32)
        else:
            text_processed += i
    return text_processed


def convert_cha_to_num(cha):
    """
    把字母转换成对应的数字
    :param cha:
    :return:
    """
    return ord(cha) - 97


def encrypt_one_character(cha, key_cha):
    """
    加密一个字母
    :param cha:
    :param key_cha:
    :return:
    """

    return chr((ord(cha) - 97 + convert_cha_to_num(key_cha)) % 26 + 97)


def decrypt_one_character(cha, key_cha):
    """
    解密一个字母
    :param cha:
    :param key_cha:
    :return:
    """

    return chr((ord(cha) - 97 - convert_cha_to_num(key_cha)) % 26 + 97)


def encrypt_one_charactoer_with_table(cha, key_cha):
    """
    使用查表的方式加密一个字母
    :param cha:
    :param key_cha:
    :return:
    """
    cha_map = []

    for i in range(26):
        cha_map.append([chr((i + x) % 26 + 97) for x in range(26)])

    return cha_map[convert_cha_to_num(cha)][convert_cha_to_num(key_cha)]


def encrypt_string(str, key):
    """
    加密经过处理过的干净的字符串
    :param str:
    :param key:
    :return:
    """
    encrypted_string = ""
    for i in range(len(str)):
        pos = i % len(key)
        encrypted_string += encrypt_one_character(str[i], key[pos])
    return encrypted_string


def decrypt_string(str, key):
    """
        解密经过处理过的干净的字符串
        :param str:
        :param key:
        :return:
        """
    encrypted_string = ""
    for i in range(len(str)):
        pos = i % len(key)
        encrypted_string += decrypt_one_character(str[i], key[pos])
    return encrypted_string


def vigenere_encry(plain_text, key):
    clean_text = convert_to_lower_case(delete_useless_cha(plain_text))
    clean_key = convert_to_lower_case(delete_useless_cha(key))
    return encrypt_string(clean_text, clean_key)


def vigenere_decry(cipher_text, key):
    clean_text = convert_to_lower_case(delete_useless_cha(cipher_text))
    clean_key = convert_to_lower_case(delete_useless_cha(key))
    return decrypt_string(clean_text, clean_key)


# a = "abcd"
# b = "key"
# print(vigenere_encry(a, b))
#
# c = "kfan"
# print(vigenere_decry(c, b))

# def mian():
#     y = input("请输入需要加密的字符:")
#     key = input("请输入密钥:")
#
#     clean_text = convert_to_lower_case(delete_useless_cha(y))
#     clean_key = convert_to_lower_case(delete_useless_cha(key))
#     print(encrypt_string(clean_text, clean_key))
#
#     y = input("请输入需要解密的字符:")
#     key = input("请输入密钥:")
#     clean_text = convert_to_lower_case(delete_useless_cha(y))
#     clean_key = convert_to_lower_case(delete_useless_cha(key))
#     print(decrypt_string(clean_text,clean_key))
#
#
# if __name__ == "__main__":
#     print(delete_useless_cha("asdfjl;dasjfoias';  l;jksdafioj"))
#     print(convert_to_lower_case("DSAFHKKASDF"))
#     print(encrypt_string("thisistheplaintext", "hold"))
#     print(decrypt_string("avtvpgekldwdpbeheh", "hold"))
#     mian()
#     input()