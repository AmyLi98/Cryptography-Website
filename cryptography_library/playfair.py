import numpy as np


def playfair_encrypt(plain_text: str, key: str) -> str:  # 贾鹏晖
    def get_rows_columns(alphabet):
        if alphabet == "j":  # 矩阵中只有25个字母，j用i代替
            alphabet = "i"
        for p in range(len(list_secret)):
            for j in range(len(list_secret[p])):
                if list_secret[p][j] == alphabet:
                    return p, j

    plain_text = plain_text.replace(" ", "").replace(",", "")      # 去掉空格和逗号
    list_plain_text = list(plain_text)                # 字符串转化成列表
    flag = False
    count = 0          # 计算列表中有多少组是不同的
    while not flag:
        for i in range(len(list_plain_text)):
            if i % 2 == 1:         # 列表中的第奇数个
                if list_plain_text[i] == list_plain_text[i - 1]:       # 第奇数个与前一个(偶数)是否相同
                    list_plain_text.insert(i, "q")        # 有重复明文字母则插入一个填充字母q 并且退出循环
                    break
                if list_plain_text[i] != list_plain_text[i - 1]:
                    count += 1
                    if count == int(len(list_plain_text) / 2):
                        flag = True
    if len(list_plain_text) % 2 == 1:         # 如果一共有奇数个字母，则填充q
        list_plain_text.append("q")

    list_key = list(key)
    list_key_clear = []
    for i in list_key:
        if i not in list_key_clear:
            list_key_clear.append(i)
    list_key.clear()
    for i in list_key_clear:
        list_key.append(i)
    for i in range(97, 106):
        if chr(i) not in list_key:
            list_key.append(chr(i))
    for i in range(107, 123):
        if chr(i) not in list_key:
            list_key.append(chr(i))
    list_secret = np.array(list_key).reshape(5, 5).tolist()
    encryption_list = []
    for i in range(len(list_plain_text)):
        if i % 2 == 0:
            x = list_plain_text[i].lower()      # 将一组字母转为小写
            y = list_plain_text[i + 1].lower()
            x_tuple = get_rows_columns(x)       # 返回元组形式
            y_tuple = get_rows_columns(y)
            if x_tuple[0] == y_tuple[0]:        # 若明文字母在矩阵中同行
                x_cipher = list_secret[x_tuple[0]][(x_tuple[1] + 1) % 5]
                y_cipher = list_secret[y_tuple[0]][(y_tuple[1] + 1) % 5]
            elif x_tuple[1] == y_tuple[1]:      # 若明文字母在矩阵中同列
                x_cipher = list_secret[(x_tuple[0] + 1) % 5][x_tuple[1]]
                y_cipher = list_secret[(y_tuple[0] + 1) % 5][y_tuple[1]]
            else:            # 若明文字母在矩阵中不同行不同列
                x_cipher = list_secret[x_tuple[0]][y_tuple[1]]
                y_cipher = list_secret[y_tuple[0]][x_tuple[1]]
            encryption_list.append(x_cipher)
            encryption_list.append(y_cipher)
    cipher_text = "".join(encryption_list)
    return cipher_text


def playfair_decrypt(cipher_text: str, key: str) -> str:  # 贾鹏晖
    def get_rows_columns(alphabet):
        if alphabet == "j":  # 矩阵中只有25个字母，j用i代替
            alphabet = "i"
        for p in range(len(list_secret)):
            for j in range(len(list_secret[p])):
                if list_secret[p][j] == alphabet:
                    return p, j

    cipher_text = cipher_text.replace(" ", "").replace(",", "")
    list_cipher_text = list(cipher_text.strip())              # 将字符串转化为列表
    list_key = list(key)
    list_key_clear = []
    for i in list_key:
        if i not in list_key_clear:
            list_key_clear.append(i)
    list_key.clear()
    for i in list_key_clear:
        list_key.append(i)
    for i in range(97, 106):
        if chr(i) not in list_key:
            list_key.append(chr(i))
    for i in range(107, 123):
        if chr(i) not in list_key:
            list_key.append(chr(i))
    list_secret = np.array(list_key).reshape(5, 5).tolist()
    decryption_list = []
    for i in range(len(list_cipher_text)):
        if i % 2 == 0:
            x = list_cipher_text[i].lower()          # 将一组字母转为小写
            y = list_cipher_text[i + 1].lower()
            x_tuple = get_rows_columns(x)            # 返回元组形式
            y_tuple = get_rows_columns(y)
            if x_tuple[0] == y_tuple[0]:             # 若密文字母在矩阵中同行
                x_open = list_secret[x_tuple[0]][(x_tuple[1] - 1) % 5]
                y_open = list_secret[y_tuple[0]][(y_tuple[1] - 1) % 5]
            elif x_tuple[1] == y_tuple[1]:           # 若密文字母在矩阵中同列
                x_open = list_secret[(x_tuple[0] - 1) % 5][x_tuple[1]]
                y_open = list_secret[(y_tuple[0] - 1) % 5][y_tuple[1]]
            else:                                    # 若密文字母在矩阵中不同行不同列
                x_open = list_secret[x_tuple[0]][y_tuple[1]]
                y_open = list_secret[y_tuple[0]][x_tuple[1]]
            decryption_list.append(x_open)
            decryption_list.append(y_open)
    if decryption_list[-1] == "q":              # 若列表最后一个元素是q，则删除
        decryption_list.pop(-1)
    delete_list = []
    for i in range(len(decryption_list)):
        if i % 2 == 0:  # 第偶数个
            if i + 2 < len(decryption_list) and \
                    decryption_list[i] == decryption_list[i + 2] and decryption_list[i + 1] == "q":
                delete_list.append(i + 1)
    delete_list.reverse()  # 反序，从后往前删除
    for i in delete_list:
        decryption_list.pop(i)
    plain_text = "".join(decryption_list)
    return plain_text


