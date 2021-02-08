from pathlib import Path
from os import makedirs, path
from flask import request, render_template, redirect, url_for
from app.ring_of_fire.utils.dbo import DBOperations
from app.ring_of_fire.utils.config import card_actions
from app.ring_of_fire.utils.tools import random_card, shuffle, top_pop, next_player

from app.ring_of_fire import ring_of_fire
from app.ring_of_fire.forms import PlayerCountForm, PlayerNameForm

cards = list()
player_config = dict()

pkg_root = path.split(__file__)[0]

player_path = Path(pkg_root, "data")
if not Path.is_dir(player_path):
    makedirs(player_path)

db_path = Path(player_path, "players.db")
db = DBOperations(db_path)


@ring_of_fire.route("/rof_home", methods=['GET', 'POST'])
def home():
    form = PlayerCountForm()
    if len(cards) == 0:
        shuffle(cards)

    if request.method == "GET":
        db.create()
        return render_template("ring_of_fire/index.html", form=form)

    player_config["THUMB"] = None
    player_config["QUESTION"] = None
    player_config["POP"] = 0
    player_config["COUNT"] = int(form.number.data)

    return redirect(url_for("ring_of_fire.assign_players"))


@ring_of_fire.route("/assign", methods=['GET', 'POST'])
def assign_players():
    number = player_config["COUNT"]
    players = {f"player{i}": f"Player {i + 1}" for i in range(number)}

    PlayerNameForm.append_class(players)
    form = PlayerNameForm()

    if request.method == "GET":
        return render_template("ring_of_fire/assign.html", players=players, form=form)

    if request.method == "POST":
        for i in range(number):
            db.insert_player(player_id=i, name=form.data.get(f"player{i}"))

        return redirect(url_for("ring_of_fire.play_rof", index=0))


@ring_of_fire.route("/play", methods=['GET', 'POST'])
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

        if card[0] == "Q":
            player_config["QUESTION"] = player[1]

        return render_template("ring_of_fire/play.html", card=card, name=player[1],
                               prompt=prompt, players=players, rules=rules,
                               thumb=player_config.get("THUMB"), question=player_config.get("QUESTION"),
                               partners=partners, pop=pop)

    rule = request.form.get("rule")
    if rule:
        db.insert_rule(player_config["INDEX"], str(rule))

    partner = request.form.get("partners")
    if partner:
        db.insert_partner(player_config["INDEX"], str(partner))

    return redirect(
        url_for(
            "ring_of_fire.play_rof", index=next_player(index=player_config["INDEX"],
                                                       count=player_config["COUNT"])
        )
    )
