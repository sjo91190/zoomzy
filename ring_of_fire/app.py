from pathlib import Path
from waitress import serve
from os import urandom, makedirs, path
from paste.translogger import TransLogger
from flask import Flask, request, render_template, redirect, url_for
from ring_of_fire.game.dbo import DBOperations
from ring_of_fire.game.config import card_actions
from ring_of_fire.game.tools import random_card, shuffle, top_pop, next_player

app = Flask(__name__)
app.secret_key = urandom(24)

cards = list()
player_config = dict()

pkg_root = path.split(__file__)[0]

player_path = Path(pkg_root, "data")
if not Path.is_dir(player_path):
    makedirs(player_path)

db_path = Path(player_path, "players.db")
db = DBOperations(db_path)


@app.route("/", methods=['GET', 'POST'])
def home():
    if len(cards) == 0:
        shuffle(cards)

    if request.method == "GET":

        db.create()
        return render_template("index.html")

    player_config["THUMB"] = None
    player_config["POP"] = 0
    player_config["COUNT"] = int(request.form.get("number"))
    return redirect(url_for("assign_players"))


@app.route("/assign", methods=['GET', 'POST'])
def assign_players():

    number = int(player_config["COUNT"])

    if request.method == "GET":
        return render_template("assign.html", number=number)

    if request.method == "POST":
        for i in range(number):
            db.insert_player(player_id=i, name=request.form.get(f"player{i}"))

        return redirect(url_for("play_rof", index=0))


@app.route("/play", methods=['GET', 'POST'])
def play_rof():

    if request.method == "GET":

        card = random_card(cards)

        player_config["INDEX"] = int(request.args["index"])
        player = db.retrieve_player(player_config["INDEX"])

        prompt = card_actions(card[0], player[1])

        players = db.all_players()
        rules = db.retrieve_rules()
        partners = db.retrieve_partners()
        pop = top_pop(player_config)

        if card[0] == "5":
            player_config["THUMB"] = player[1]

        return render_template("play.html", card=card, name=player[1],
                               prompt=prompt, players=players, rules=rules,
                               thumb=player_config.get("THUMB"), partners=partners,
                               pop=pop)

    rule = request.form.get("rule")
    if rule:
        db.insert_rule(player_config["INDEX"], str(rule))

    partner = request.form.get("partners")
    if partner:
        db.insert_partner(player_config["INDEX"], str(partner))

    return redirect(
        url_for(
            "play_rof", index=next_player(index=player_config["INDEX"],
                                          count=player_config["COUNT"])
        )
    )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    serve(TransLogger(app), host=host, port=port)
