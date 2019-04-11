from random import randint
from collections import Counter


class Roller:

    def __init__(self, seed=20):
        if isinstance(seed, str) and 'd' in seed:
            self.seed = (1, int(seed.split("d")[1]))
        else:
            self.seed = (1, seed)

    def __repr__(self):
        return "d{seed}".format(seed=self.seed[1])

    @property
    def roll(self):
        return randint(*self.seed)

    @property
    def high(self):
        return self.seed[1]

    @property
    def low(self):
        return self.seed[0]

    def check_roll(self, modifier=0):
        return "{roll}+{mod}".format(roll=self.roll, mod=modifier)

    def check(self, dc=0, modifier=0, critical=20):
        check_roll = self.check_roll(modifier=modifier)
        roll, bonus = map(int, check_roll.split("+"))
        full = roll + bonus
        return "nat1" if roll == 1 else "crit" if roll >= critical else check_roll, full >= dc
