from flask import Flask, request, render_template, jsonify, abort
from roller import Roller
from attack import Attack


app = Flask(__name__)

def arg_value(arg, default=None, type=int):
    return request.args.get(arg, default, type=int)


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route('/check')
def check():
    seed = arg_value('seed', 20, type=int)
    roller = Roller(seed)
    dc = arg_value('dc', 0, type=int)
    roll, beats_dc = roller.check(dc=dc,
                                  modifier=arg_value('modifier', 0, type=int),
                                  critical=arg_value('critical', 20, type=int))
    succeeds = "" if dc == 0 else "Succeeds" if beats_dc else "Fails"
    return jsonify({'return': "{roll} {succeeds}".format(roll=roll, succeeds=succeeds)}), 200


@app.route('/attacks')
def attacks():
    hit_roller = Roller('d20')
    dmg_seed = arg_value('dmg_seed', 2)
    attacker = Attack([Roller("d{dmg}".format(dmg=dmg_seed)) for _ in range(arg_value('n_dmg_rollers', 1))],
                      damage_modifier=arg_value('dmg_modifier', 0))
    attacks = attacker.attacks(hit_roller,
                               arg_value('n_attacks', 1),
                               risk_buffer=arg_value('risk_buffer', 0),
                               dc=arg_value('dc', 0),
                               modifier=arg_value('hit_modifier', 0),
                               critical=arg_value('critical', 20))
    return jsonify({'return': attacker.html_attacks(attacks)}), 200

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
