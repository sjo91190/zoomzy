import random
from pathlib import Path
from os import urandom, mkdir
from waitress import serve
from paste.translogger import TransLogger
from flask import Flask, request, render_template, redirect, url_for, session, json
from ring_of_fire.deck import deck
from ring_of_fire.dbo import DBOperations
from ring_of_fire.config import card_actions

app = Flask(__name__)
app.secret_key = urandom(24)

cards = deck()
player_config = dict()

path = Path("ring_of_fire", "data")
if not Path.is_dir(path):
    mkdir(path)

db_path = Path(path, "players.db")
player_db = DBOperations(db_path)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":

        player_db.create()
        return render_template("index.html")

    player_config["COUNT"] = int(request.form.get("number"))
    return redirect(url_for("assign_players"))


@app.route("/assign", methods=['GET', 'POST'])
def assign_players():

    number = int(player_config["COUNT"])

    if request.method == "GET":
        return render_template("assign.html", number=number)

    if request.method == "POST":
        for i in range(number):
            player_db.insert(player_id=i, name=request.form.get(f"player{i}"))

        return redirect(url_for("play_rof", index=0))


@app.route("/play", methods=['GET', 'POST'])
def play_rof():

    if request.method == "GET":

        card = random_card()

        player_config["INDEX"] = int(request.args["index"])
        player = player_db.retrieve(player_config["INDEX"])

        prompt = card_actions(card[0], player[1])

        return render_template("play.html", card=card, name=player[1], prompt=prompt)

    return redirect(
        url_for(
            "play_rof", index=next_player(index=player_config["INDEX"])
        )
    )


def random_card():

    if len(cards) == 0:
        return "END OF DECK"

    card = random.choice(cards)
    cards.remove(card)

    return card


def next_player(index):
    count = (player_config["COUNT"] - 1)
    if index < count:
        return index + 1

    return 0


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    serve(TransLogger(app), host=host, port=port)
