import codecs

MAX = 256   #定义全局的数组长度控制变量MAX

def KSA(key):
    """
        :param key: 密钥
        :return: S 数组

        Key Scheduling Algorithm:(伪代码)
        for i from 0 to 255
            S[i] := i
        endfor
        j := 0
        for i from 0 to 255
            j := (j + S[i] + key[i mod keylength]) mod 256
            swap values of S[i] and S[j]
        endfor
    """

    key_length = len(key)
    # 创建 S 数组
    S = list(range(MAX))  # [0,1,2, ... , 255]
    j = 0
    for i in range(MAX):
        j = (j + S[i] + key[i % key_length]) % MAX
        S[i], S[j] = S[j], S[i]  # 交换值

    return S


def PRGA(S):
    """
        :param S: 数组
        :return: K 数组

        Psudo Random Generation Algorithm:
        i := 0
        j := 0
        while GeneratingOutput:
            i := (i + 1) mod 256
            j := (j + S[i]) mod 256
            swap values of S[i] and S[j]
            K := S[(S[i] + S[j]) mod 256]
            output K
        endwhile
    """

    i = 0
    j = 0
    while True:
        i = (i + 1) % MAX
        j = (j + S[i]) % MAX

        S[i], S[j] = S[j], S[i]  # 交换值
        K = S[(S[i] + S[j]) % MAX]
        yield K # yield 是一个类似 return 的关键字，只是这个函数返回的是个生成器，当你使用for进行迭代的时候，函数中的代码才会执行


def get_keystream(key):
    """
        :param key: 密钥
        :get: 使用 PRGA 生成的密钥流
        :return: 生成器
    """

    S = KSA(key)
    return PRGA(S)


def encrypt_flow(text, key):
    """
        加密流程
        :param text: 待加密/解密的Unicode/字符串数组
        :param key: 密钥，字符串
        :return:
    """

    key = [ord(c) for c in key]
    keystream = get_keystream(key)  #生成密钥流

    res = []
    for c in text:
        # X 表示以十六进制形式输出 02 表示不足两位,前面补0输出;
        val = ("%02X" % (c ^ next(keystream)))  # XOR 操作并且输出十六进制数
        res.append(val)
    return ''.join(res)


def RC4_encrypt(plaintext, key):
    """
        :param plaintext: 待加密的明文字符串
        :param key: RC4加密使用的密钥，字符串
        :return:
    """

    plaintext = [ord(c) for c in plaintext]
    return encrypt_flow(plaintext, key)


def RC4_decrypt(ciphertext, key):
    """
            :param ciphertext: 用RC4加密的密文字符串
            :param key: RC4加密使用的密钥，字符串
            :return:
        """

    ciphertext = codecs.decode(ciphertext, 'hex_codec') # 16进制密文字符串转成 byte 类型
    res = encrypt_flow(ciphertext, key)
    return codecs.decode(res, 'hex_codec').decode('utf-8')  # 16进制密文字符串转成 byte 类型，再转成 utf-8 类型

'''
example:
    key = 'not-so-random-key'
    plaintext = 'Good work! Your implementation is correct'
    cipher_text = '2D7FEE79FFCE80B7DDB7BDA5A7F878CE298615476F86F3B890FD4746BE2D8F741395F884B4A35CE979'
'''