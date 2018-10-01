def delete_useless_cha(text):
    """
    删除读取字符串中非英文字母的字符
    :param text:要处理的字符串文本
    :return:处理后的字符串文本
    """
    text_processed = ""
    for i in text:
        if (ord(i) >= 65 and ord(i) <= 90) or (ord(i) <= 122 and ord(i) >= 97):
            text_processed += i
    return text_processed


def convert_to_lower_case(text):
    """
    把字符中大写字母转换成小写字母
    :param text:待处理的字符串文本
    :return:均为小写字母的字符串文本
    """
    text_processed = ""
    for i in text:
        if ord(i) >= 65 and ord(i) <= 90:
            text_processed += chr(ord(i) + 32)
        else:
            text_processed += i
    return text_processed


def convert_cha_to_num(character):
    """
    把字母转换成对应的数字
    :param character:
    :return:
    """
    return ord(character) - 97


def encrypt_one_character(character, key_character):
    """
    加密一个字母
    :param character:
    :param key_character:
    :return:
    """

    return chr((ord(character) - 97 + convert_cha_to_num(key_character)) % 26 + 97)


def decrypt_one_character(character, key_character):
    """
    解密一个字母
    :param character:
    :param key_character:
    :return:
    """

    return chr((ord(character) - 97 - convert_cha_to_num(key_character)) % 26 + 97)


def autokey_cipher_encrypt(plain_text, key):
    """
    :param plain_text: 明文
    :param key: 密钥
    :return:加密密文
    """
    #在加密算法之前对所有的字符进行标准化处理
    plaintext = convert_to_lower_case(delete_useless_cha(plain_text))
    clean_key = convert_to_lower_case(delete_useless_cha(key))

    # 保证文本内容不存在空格
    plaintext = plaintext.replace(" ", "")
    clean_key = clean_key.replace(" ", "")

    if plaintext.isalpha():
       if clean_key.isalpha():
           # 首先要对key进行处理，使用plaintext法
           if len(plaintext) > len(clean_key):
               add_len = len(plaintext) - len(clean_key)
               clean_key += plaintext[0:add_len]

           cipher_text = ""
           for i in range(len(plaintext)):
               cipher_text += encrypt_one_character(plaintext[i], clean_key[i])
       else:    #错误处理
           print("Enter valid key, only letters are allowed !!")
           return ""
    else:
        print("Enter valid plain_text, only letters are allowed !!")
        return ""

    return cipher_text


def autokey_cipher_decrypt(cipher_text, key):
    """
    :param cipher_text: 密文
    :param key: 密钥
    :return: 明文
    """

    # 在解密算法之前对字符进行标准化处理
    clean_text = convert_to_lower_case(delete_useless_cha(cipher_text))
    clean_key = convert_to_lower_case(delete_useless_cha(key))

    # 保证文本内容不存在空格
    clean_text = clean_text.replace(" ", "")
    clean_key = clean_key.replace(" ", "")

    if clean_text.isalpha():
       if clean_key.isalpha():
           # 首先要对key进行处理，使用plaintext法
           if len(clean_text) > len(clean_key):
               add_len = len(clean_text) - len(clean_key)
               clean_key += clean_text[0:add_len]

           plaintext = ""
           for i in range(len(clean_text)):
               # pos = i % len(key)
               plaintext += decrypt_one_character(clean_text[i], clean_key[i])
       else:    #错误处理
           print("Enter valid key, only letters are allowed !!")
           return ""
    else:
        print("Enter valid cipher_text, only letters are allowed !!")
        return ""

    return plaintext
