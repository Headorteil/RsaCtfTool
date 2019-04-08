#! /usr/bin/env python3
import gmpy2
import binascii

class chinese_attack():

    def __init__(self, attackobjs):
        self.ln = [1]*len(attackobjs)
        self.len = len(attackobjs)
        self.ntot = 1
        self.m = 0
        self.test = False
        self.attackobjs = attackobjs

    def system_solve(self):
        """ This function find the solution of the congruency system """
        for i in range(self.len):
            self.ntot *= self.attackobjs[i].pub_key.n
            for j in range(self.len):
                if i != j:
                    self.ln[i] *= self.attackobjs[j].pub_key.n
        for i in range(self.len):
            self.ln[i] *= gmpy2.invert(self.ln[i], self.attackobjs[i].pub_key.n)
        for i in range(self.len):
            self.m += self.attackobjs[i].cipherdec * self.ln[i]
        self.m = self.m % self.ntot
        self.m, self.test = gmpy2.iroot(self.m, 3)
        if not self.test:
            print("Miscalculation")
            exit()

    def print_value(self):
        self.m=str(hex(self.m))[2:] #long
        self.m=binascii.unhexlify(self.m)
        return self.m

