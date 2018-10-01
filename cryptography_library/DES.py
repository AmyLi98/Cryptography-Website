import random

"""key = self.PC_1(full_key=self.short_key_to_long(key))
        k1 = self.shift(key[0:28]) + self.shift(key[28:])"""


def xor(x, y):
    if x == y:
        return '0'
    return '1'


class DES:
    def create_short_key(self):
        KEY_LENGTH = 7
        NUMBER_RANGE = 16
        num_list = []
        for i in range(NUMBER_RANGE):
            num_list.append(i)

        key = ''
        for _ in range(KEY_LENGTH * 2):
            single_key = bin(random.choice(num_list))[2:]
            for _ in range(4 - len(single_key)):  # 补满四位长度
                single_key = '0' + single_key
            key = key + single_key
        return key

    def short_key_to_long(self, short_key):
        assert len(short_key) == 56

        def short_to_long(seven):
            """
            length has to be seven
            :param seven:
            :return:
            """
            assert len(seven) == 7
            num_of_zero = 0
            for i in seven:
                if i == '0':
                    num_of_zero += 1

            if (num_of_zero % 2) == 0:
                seven = seven + '0'
                return seven

            seven = seven + '1'
            return seven

        full_key = ''
        for i in range(8):
            full_key = full_key + short_to_long(short_key[7 * i:7 * (i + 1)])
        assert len(full_key) == 64
        return full_key

    def PC_1(self, full_key):
        """

        :param full_key: 64 bit key
        :return:
        """
        key_converted = ''
        convert_box = [57, 49, 41, 33, 25, 17, 9,
                       1, 58, 50, 42, 34, 26, 18,
                       10, 2, 59, 51, 43, 35, 27,
                       19, 11, 3, 60, 52, 44, 36,
                       63, 55, 47, 39, 31, 23, 15,
                       7, 62, 54, 46, 38, 30, 22,
                       14, 6, 61, 53, 45, 37, 29,
                       21, 13, 5, 28, 20, 12, 4]
        for i in convert_box:
            key_converted = key_converted + full_key[i - 1]

        return key_converted

    def PC_2(self, key):
        """

        :param key:56 bit one
        :return:
        """
        assert len(key) == 56
        compress_box = [14, 17, 11, 24, 1, 5, 3, 28,
                        15, 6, 21, 10, 23, 19, 12, 4,
                        26, 8, 16, 7, 27, 20, 13, 2,
                        41, 52, 31, 37, 47, 55, 30, 40,
                        51, 45, 33, 48, 44, 49, 39, 56,
                        34, 53, 46, 42, 50, 36, 29, 32]
        key_converted = ''
        for i in compress_box:
            key_converted = key_converted + key[i - 1]

        assert len(key_converted) == 48
        return key_converted

    def create_full_key(self):
        return self.short_key_to_long(self.create_short_key())

    def initial_transpostion(self, plain_text):

        transpose_box = [58, 50, 42, 34, 26, 18, 10, 2,
                         60, 52, 44, 36, 28, 20, 12, 4,
                         62, 54, 46, 38, 30, 22, 14, 6,
                         64, 56, 48, 40, 32, 24, 16, 8,
                         57, 49, 41, 33, 25, 17, 9, 1,
                         59, 51, 43, 35, 27, 19, 11, 3,
                         61, 53, 45, 37, 29, 21, 13, 5,
                         63, 55, 47, 39, 31, 23, 15, 7]
        text_transposed = ''
        for i in transpose_box:
            text_transposed = text_transposed + plain_text[i - 1]
        return text_transposed

    def EBox(self, string):
        """

        :param string:
        :return:
        """
        assert len(string) == 32
        expanded_string = ''
        for i in range(int(32 / 4)):
            expanded_string = expanded_string + string[4 * i - 1] + string[4 * i:4 * (i + 1)] + string[
                (4 * (i + 1)) % 32]

        return expanded_string

    def SBox(self, key, text):
        def six_to_four(string, box):
            x = bin(box[int(string[0] + string[-1], 2)][int(string[1:5], 2)])
            x = x[2:]
            for i in range(4 - len(x)):
                x = '0' + x
            return x

        TEXT_LENGTH = 48
        text_after_xor = ''
        for i in range(TEXT_LENGTH):
            text_after_xor = text_after_xor + xor(key[i], text[i])

        S_BOX = [

            [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
             ],

            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
             ],

            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
             ],

            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
             ],

            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
             ],

            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
             [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
             ],

            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
             ],

            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
             ]
        ]

        output = ''
        for i in range(8):
            output = output + six_to_four(text_after_xor[6 * i: 6 * (i + 1)], S_BOX[i])
        assert len(output) == 32
        return output

    def PBox(self, text):
        P_box = [16, 7, 20, 21, 29, 12, 28, 17,
                 1, 15, 23, 26, 5, 18, 31, 10,
                 2, 8, 24, 14, 32, 27, 3, 9,
                 19, 13, 30, 6, 22, 11, 4, 25]

        output = ''
        for i in P_box:
            output = output + text[i - 1]
        assert len(output) == 32
        return output

    def final_transpositon(self, text):
        t_box = [40, 8, 48, 16, 56, 24, 64, 32,
                 39, 7, 47, 15, 55, 23, 63, 31,
                 38, 6, 46, 14, 54, 22, 62, 30,
                 37, 5, 45, 13, 53, 21, 61, 29,
                 36, 4, 44, 12, 52, 20, 60, 28,
                 35, 3, 43, 11, 51, 19, 59, 27,
                 34, 2, 42, 10, 50, 18, 58, 26,
                 33, 1, 41, 9, 49, 17, 57, 25]
        output = ''
        for i in t_box:
            output = output + text[i - 1]
        return output

    def shift(self, key, length):
        out = ''
        for i in range(len(key)):
            out = out + key[(i + length) % len(key)]
        return out

    def shift_r(self, key, length):
        out = ''
        for i in range(len(key)):
            out = out + key[(i - length) % len(key)]
        return out

    def single_stage(self, key, lp, rp):
        """
        单次加密一轮
        :param key: 48 bit
        :param rp: 32 bit
        :return:
        """

        expand_r = self.EBox(rp)
        x = self.SBox(key, expand_r)
        x = self.PBox(x)
        assert len(x) == 32
        t = ''
        for i in range(len(x)):
            t = t + xor(lp[i], x[i])
        x = t
        assert len(x) == 32

        return x, rp

    def right_part(self, key, text, en=1):
        """

        :param key: 32 bit
        :param text: 64 bit
        :return:
        """
        assert len(text) == 64
        lp, rp = text[0:32], text[32:]
        assert len(lp) == 32
        assert len(rp) == 32
        shift_length = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        shift_r_l = [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        c = key[0:28]
        d = key[28:]
        c_list = []
        d_list = []
        for i in range(16):
            if en:
                c = self.shift(c, shift_length[i])
                d = self.shift(d, shift_length[i])
                c_list.append(c)
                d_list.append(d)
            else:
                c = self.shift_r(c, shift_r_l[i])
                d = self.shift_r(d, shift_r_l[i])
                c_list.append(c)
                d_list.append(d)
        for i in range(16):
            assert len(d) == 28
            key = self.PC_2(c_list[i] + d_list[i])
            lp, rp = self.single_stage(key, lp, rp)
            assert len(lp) == 32
            assert len(rp) == 32
        return self.final_transpositon(lp + rp)

    def encrypt(self, full_key, text, en=1):
        f = self.PC_1(full_key)
        output = ''
        for i in range(int(len(text) / 64)):
            part_of_text = text[64 * i: 64 * (i + 1)]
            assert len(part_of_text) == 64
            part_of_text = self.initial_transpostion(part_of_text)
            output = output + self.right_part(f, part_of_text, en)
        return output

    def encrypt_(self, full_key, data: bytes):
        bin(int(str(data), base=16))

    def test(self):
        self.create_short_key()
        self.PC_1(self.create_full_key())
        self.short_key_to_long(self.create_short_key())
        self.PC_2(self.create_short_key())
        self.initial_transpostion(self.create_full_key())
        self.EBox(self.create_full_key()[0:32])
        self.SBox(self.EBox(self.create_full_key()[0:32]), self.EBox(self.create_full_key()[0:32]))

    def encrypt_file(self, file_data: bytes, key: str):
        import sys
        # print(file_data)
        k_lenth = len(file_data)
        key_b = key[:56]
        # print(file_data)
        file_data = bin(int.from_bytes(file_data, byteorder="little"))
        # print(file_data)
        f_length = len(file_data)
        num_zero = 64 - (f_length % 64)
        # print(file_data)

        for i in range(num_zero):
            file_data = file_data + '0'
        encrypt_time = int(len(file_data) / 64)

        encrypt_text = ""

        full_key = self.short_key_to_long(key_b)
        for i in range(encrypt_time):
            encrypt_text += self.encrypt(full_key, file_data[i * 64:(i + 1) * 64])
        # print(encrypt_text)
        return str(num_zero) + '\n' + str(k_lenth) + '\n' + encrypt_text

    def decrypt_file(self, file_data: str, key: str):
        file_data = file_data.split('\n')
        # print("len _file data", len(file_data))
        # print("file data", file_data)
        zeros = int(file_data[0])
        k_length = int(file_data[1])
        k = file_data[2]
        key_b = key[:56]
        full_key = self.short_key_to_long(key_b)
        decrypt_txt = ""
        for i in range(int(len(k) / 64)):
            decrypt_txt += self.encrypt(full_key, k[i * 64:(i + 1) * 64], 0)

        # print(decrypt_txt)
        # print(decrypt_txt[:-zeros])
        decrypt_txt = '0b' + decrypt_txt[2:]
        y = int(decrypt_txt[:-zeros], 2).to_bytes(len(decrypt_txt[:-zeros]) // 8, byteorder='little')[:k_length]
        # print(y)
        # print("len", len(y))
        return y


if __name__ == "__main__":
    print(bin(int(str('sdasfas'.encode('utf-8')), base=16)))
    des = DES()
    print(len(des.create_short_key()))
    import binascii

    print(binascii.a2b_uu(des.create_short_key()))
    # text = '0000000100100011010001010110011110001001101010111100110111101111'
    # key = '0001001100110100010101110111100110011011101111001101111111110001'
    # print(text)
    # print(len(key))
    # z = des.encrypt(key, text)
    # print(z)
    # z = des.encrypt(key, z, 1)
    # print(z)
