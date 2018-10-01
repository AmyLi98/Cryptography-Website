import numpy as np
from cryptography_library.vigenere import delete_useless_cha,convert_to_lower_case

def convert_letters_to_nums(key):
    """
    把字母转换成排序用的数字
    :param key:
    :return: list
    """
    sorted_list = sorted([i for i in key])
    num_list = []
    for i in key:
        num_list.append(sorted_list.index(i))
        sorted_list[num_list[-1]] = 0

    return num_list

def get_reverse_index(key):
    """
    获取反向的index用于解密
    :param key:
    :return:
    """
    normal_index = convert_letters_to_nums(key)
    reverse_index = []
    for i in range(len(normal_index)):
        reverse_index.append(normal_index.index(i))

    return reverse_index

def convert_string_to_matrix(text,key_lenth):
    """
    把文字转换成矩阵形式
    :param text:
    :param key_lenth:
    :return:
    """

    text_matrix = np.array([i for i in text])
    text_matrix = np.reshape(text_matrix, (-1,key_lenth))
    return text_matrix

def fix_text_lenth(text,key_lenth):
    """
    如果无法整除则进行填充 x
    :param text:
    :param key_lenth:
    :return:
    """

    if len(text)%key_lenth == 0:
        return text

    for i in range(key_lenth - len(text)%key_lenth):
        text += "x"

    return text

def change_pos(matrix,index_list):
    """
    根据key生成的数字列表重新排列
    :param matrix:
    :param index_list:
    :return:
    """
    return matrix[index_list]



def encrypt(text,key):
    index = convert_letters_to_nums(key)
    text = fix_text_lenth(text,len(key))
    matrix = convert_string_to_matrix(text,len(key))
    return change_pos(matrix.transpose(),index).reshape(-1)

def decrypt(text,key):
    reverse_index = get_reverse_index(key)
    matrix = np.array([i for i in text]).reshape(len(key),-1)
    return change_pos(matrix,reverse_index).transpose().reshape(-1)


def column_encry(plaintext, key):
    return "".join(encrypt(delete_useless_cha(plaintext), key))


def column_decry(ciphertext, key):
    return "".join(decrypt(ciphertext, key))


# if __name__ == "__main__":
#     # print(convert_letters_to_nums("adfawe"))
#     # print(np.arange(8).reshape((4,-1)))
#     # print(convert_string_to_matrix(fix_text_lenth("fadsfasdfasdfasfasdfsd",3),3))
#     y = input("请输入需要加密的字符:")
#     key = input("请输入密钥:")
#
#     print("".join(encrypt(delete_useless_cha(y), key)))
#
#     y = input("请输入需要解密的字符:")
#     key = input("请输入密钥:")
#
#     print("".join(decrypt(y,key)))
#     # print(convert_letters_to_nums("experiment"))
#     input()