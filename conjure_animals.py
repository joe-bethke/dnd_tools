from random import randint
from roller import Roller
from attack import Attack

x = Attack([Roller('d6'), Roller('d6'), Roller('d6')], damage_modifier=2)
hit_roller = Roller('d20')

for i in x.attacks(hit_roller, 10, dc=0, modifier=3, critical=18):
    print(i)
