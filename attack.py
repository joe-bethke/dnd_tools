import pandas as pd

class Attack:

    def __init__(self, damage_rollers, damage_modifier=0):
        self.damage_rollers = damage_rollers
        self.damage_modifier = damage_modifier

    @staticmethod
    def html_attacks(attacks):
        records = [{'Attacker': attacker, 'Roll': roll, 'Damage': damage}
                   for attacker, roll, damage in attacks]
        df = pd.DataFrame.from_records(records, index='Attacker')
        return df.to_html()

    def damage(self, hit_roll, risk_buffer=0):
        damage = 0
        for roller in self.damage_rollers:
            rolled_damage = roller.roll
            damage += rolled_damage
            if hit_roll == "crit":
                if rolled_damage >= (roller.high // 2) - risk_buffer:
                    damage += rolled_damage
                else:
                    damage += roller.roll
        return damage + self.damage_modifier

    def attacks(self, hit_roller, n_attacks, risk_buffer=0, **hit_check):
        for attack_number in range(1, n_attacks + 1):
            roll, hit = hit_roller.check(**hit_check)
            if hit or roll == 'nat1':
                yield (attack_number, roll, self.damage(roll, risk_buffer=risk_buffer))