import hashlib
import os
import sys
import random
from Crypto.Cipher import AES
from Crypto import Random


class RSA:
    def random_prime(self):
        n = random.randint(10**10+1,10**11)
        while not self.is_prime(n):
            n = random.randint(10**10+1,10**11)

    def is_prime(self,num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num**0.5)+2, 2):
            if num % n == 0:
                return False
        return True

    def __init__(self):       
        self.q = self.random_prime()
	while 1:
	        self.p = self.random_prime()
		if self.q != self.p:
			break


    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def multiplicative_inverse(e, phi):
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        temp_phi = phi    
        while e > 0:
            temp1 = temp_phi/e
            temp2 = temp_phi - temp1 * e
            temp_phi = e
            e = temp2        
            x = x2- temp1* x1
            y = d - temp1 * y1        
            x2 = x1
            x1 = x
            d = y1
            y1 = y    
        if temp_phi == 1:
            return d + phi

    def generate_keypair(self):
        if self.p == self.q:
            raise ValueError('p and q cannot be equal')
        n = self.p * self.q
        phi = (self.p-1) * (self.q-1)
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = gcd(e, phi)
        d = multiplicative_inverse(e, phi)
        #returns pub , prv
        return ((e, n), (d, n))

    def encrypt(pk, plaintext):#public
        key, n = pk
        cipher = [(ord(char) ** key) % n for char in plaintext]
        return cipher

    def decrypt(pk, ciphertext):#private
        key, n = pk
        plain = [chr((char ** key) % n) for char in ciphertext]    
        return ''.join(plain)
   
class AESClass:

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]