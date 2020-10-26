import sys
from json import loads
import random
from ring_of_fire.deck import deck
from os import urandom
from waitress import serve
from paste.translogger import TransLogger
from flask import Flask, request, render_template, redirect, url_for, session, json

app = Flask(__name__)
app.secret_key = urandom(24)

cards = deck()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")

    return redirect(url_for("assign_players", count=request.form.get("number")))


@app.route("/assign", methods=['GET', 'POST'])
def assign_players():
    all_players = list()
    number = int(request.args["count"])

    if request.method == "GET":
        return render_template("assign.html", number=number)

    if request.method == "POST":
        for _ in range(number):
            # all_players[f"player{_}"] = request.form.get(f"player{_}")
            all_players.append(request.form.get(f"player{_}"))

        player_string = ",".join(all_players)

        return redirect(url_for("play_rof", players=player_string))


@app.route("/play", methods=['GET', 'POST'])
def play_rof():

    if request.method == "GET":

        card = random_card()
        player = request.args["players"].split(",")[0]
        return render_template("play.html", card=card, name=player)

    return redirect(
        url_for(
            "play_rof", players=current_player(
                request.args["players"].split(",")
            )
        )
    )


def random_card():

    if len(cards) == 0:
        return "END OF DECK"

    card = random.choice(cards)
    cards.remove(card)

    return card


def current_player(player_list):
    new_list = player_list
    new_list.append(player_list[0])
    del new_list[0]

    return ",".join(new_list)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    serve(TransLogger(app), host=host, port=port)
