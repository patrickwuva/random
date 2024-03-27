import random
import math



class secret:

    def __init__(self, m):
        self.m = m
        self.p = 179856#self.get_prime()
        self.q = 423471#self.get_prime()
        self.n = self.p * self.q
        self.e = 65537
        self.t = (self.p - 1) * (self.q - 1)
        self.d = pow(self.e, -1, self.t)
        self.encrypt() 

    def encrypt(self):
        self.a = int(''.join(format(ord(c), '03d') for c in self.m))
        self.c = pow(self.a, self.e, self.n)
        print(f"c: {self.c} a: {self.a}")
    
    def decrypt(self):
        self.d_m = pow(self.c, self.d, self.n)
        self.m_p = ''.join(chr(int(str(self.d_m)[i:i+3])) for i in range(0, len(str(self.d_m)), 3))
    def get_prime(self):
        p = random.randint(100000,1000000)
        for n in range(2, p // 2 + 1):
            if n % p == 0:
                self.get_prime()
        return p
    
def main():
    
    #m = input("Enter message: ")
    rsa = secret("hi")

    #print(f"msg ascii: {rsa.a} encrypted: {rsa.c}") 
    rsa.decrypt()
    print((rsa.e * rsa.d) % rsa.t)
    print(f"p: {rsa.p} q: {rsa.q} e: 65537 C: {rsa.c} t: {rsa.t} d: {rsa.d} n: {rsa.n} d_a: {rsa.d_m} pt: {rsa.m_p}")
    print(f"decrypted msg: {rsa.d_m}") 
if __name__ == "__main__":
    main()
