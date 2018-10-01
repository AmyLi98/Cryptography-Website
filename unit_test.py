import unittest
from full_functions import *
from cryptography_library.rsa import return_key


class TestStringMethods(unittest.TestCase):

    def test_caesar_cipher(self):
        message = "abcdef"
        key = "1"
        self.assertEqual(message, caesar_cipher_decrypt(caesar_cipher_encrypt(message, key), key))

    def test_keyword_cipher(self):
        message = "abcdef"
        key = "count"
        self.assertEqual(message, keyword_cipher_decrypt(keyword_cipher_encrypt(message, key), key))

    def test_playfair_cipher(self):
        message = "abccdeef"
        key = "baby"
        self.assertEqual(message, play_fair_decrypt(play_fair_encrypt(message, key), key))

    def test_vigenere(self):
        message = "abcdef"
        key = "key"
        self.assertEqual(message, vigenere_decrypt(vigenere_encrypt(message, key), key))

    def test_column(self):
        message = "abcdefghi"
        key = "key"
        self.assertEqual(message, coloumn_permutation_decrypt(coloumn_permutation_encrypt(message, key), key))

    def test_double_transposition(self):
        message = "abcdefghi"
        key = "key"
        self.assertEqual(message, double_transposition_decrypt(double_transposition_encrypt(message, key), key))

    def test_des_cipher(self):
        message = "fbgccdeeb"
        key = "ffffffffffffffff"
        self.assertEqual(message, DES_decrypt(DES_encrypt(message, key), key))

    def test_rc4(self):
        message = "abcdefghi"
        key = "key"
        self.assertEqual(message, double_transposition_decrypt(double_transposition_encrypt(message, key), key))

    def test_rsa_cipher(self):
        message = "fbgccdeeb"
        key1, key2 = return_key()
        pubkey = str(key1)
        prikey = str(key2)
        self.assertEqual(message, RSA_cipher_decrpt(RSA_cipher_encrypt(message, pubkey), prikey))


if __name__ == '__main__':
    unittest.main()
