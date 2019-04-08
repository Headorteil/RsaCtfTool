#! /usr/bin/env python3
import gmpy2
import binascii

class CommonModulusAttack():

    def __init__(self, attackobjs):
           self.a = 0
           self.b = 0
           self.m = 0
           self.i = 0
           self.attackobjs = attackobjs
           self.n = attackobjs[0].pub_key.n
           [self.e1, self.e2] = [ attackobjs[u].pub_key.e for u in range(2)]
           [self.c1, self.c2] = [ attackobjs[u].cipherdec for u in range(2)]

    def gcd(self, num1, num2):
           """
           This function os used to find the GCD of 2 numbers.
           """
           if num1 < num2:
               num1, num2 = num2, num1
           while num2 != 0:
               num1, num2 = num2, num1 % num2
           return num1

    def extended_euclidean(self):
           """
           The value a is the modular multiplicative inverse of e1 and e2.
           b is calculated from the eqn: (e1*a) + (e2*b) = gcd(e1, e2)
           e1: exponent 1
           e2: exponent 2
           """
           self.a = gmpy2.invert(self.e1, self.e2)
           self.b = (float(self.gcd(self.e1, self.e2)-(self.a*self.e1)))/float(self.e2)

    def modular_inverse(self):
           """
           i is the modular multiplicative inverse of c2 and N.
           i^-b is equal to c2^b. So if the value of b is -ve, we
           have to find out i and then do i^-b.
           Final plain text is given by m = (c1^a) * (i^-b) %N
           c1: cipher text 1
           c2: cipher text 2
           n: Modulus
           """
           i = gmpy2.invert(self.c2, self.n)
           mx = pow(self.c1, self.a, self.n)
           my = pow(i, int(-self.b), self.n)
           self.m= mx * my % self.n

    def print_value(self):
        self.m=str(hex(self.m))[2:] #long
        self.m=binascii.unhexlify(self.m)
        return self.m

