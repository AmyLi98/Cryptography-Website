import binascii

from cryptography_library.rsa import rapid_exp
import os


class DHKeyExchange:
    m = {
        "prime": 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF,
        "generator": 2
    }

    def __init__(self):
        self.__set_private_key()

    def __set_private_key(self):
        self.p = int(binascii.hexlify(os.urandom(16)), base=16)
        return self.p

    def get_public_one(self):
        return rapid_exp(self.m["generator"], self.p, self.m["prime"])

    def get_shared_key(self, other_one):
        return rapid_exp(other_one, self.p, self.m["prime"])


if __name__ == '__main__':
    print(rapid_exp(2, 2, 3))
    a = DHKeyExchange()
    b = DHKeyExchange()
    pa = a.get_public_one()
    pb = b.get_public_one()
    c = a.get_shared_key(pb)
    d = b.get_shared_key(pa)
    print(c, d)
    assert c == d

    # print(a.get_private_key())
