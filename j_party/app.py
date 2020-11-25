import random
from uuid import uuid4
from json import loads, dumps
from pathlib import Path
from os import urandom, makedirs
from flask import Flask, request, render_template, redirect, url_for
from j_party.game.dbo import JPartyOperations, PlayerOperations

app = Flask(__name__)
app.secret_key = urandom(24)

data_path = Path("j_party", "database")

data_db_path = Path(data_path, "jpartydata.db")
data_db = JPartyOperations(data_db_path)

path = Path("j_party", "data")
if not Path.is_dir(path):
    makedirs(path)

player_db_path = Path(path, "players.db")
player_db = PlayerOperations(player_db_path)

rounds = ["first", "second", "final"]


def play_set():
    show_num = data_db.show_numbers()
    _set = random.choice(show_num)

    def get_data(_round):

        _game = dict()
        game = dict()

        round_data = data_db.select_all(_set, _round)

        category = list(set(_['category'] for _ in round_data))

        for cat in category:
            _game[cat] = list()
            for data in round_data:
                if data['category'] == cat:
                    _game[cat].append(dict(value=data['value'],
                                           question=data['question'],
                                           answer=data['answer'],
                                           question_id=str(uuid4()),
                                           active=True))

            if _round == "first" or _round == "second":
                game[cat] = sorted(_game[cat], key=lambda v: int(v['value'].strip("$").replace(",", "")))
            else:
                game = _game

        return game

    for item in rounds:
        player_db.insert_game_data(item, str(dumps(get_data(item))))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        player_db.create()
        play_set()

        return render_template("assign.html")

    if request.method == "POST":
        for i in range(3):
            player_db.insert_player(name=request.form.get(f"player{i}"))

    return redirect(url_for("jparty"))


@app.route("/play", methods=['GET', 'POST'])
def jparty():
    details = player_db.retrieve_dataset('first')
    players = player_db.retrieve_score()

    if request.method == "GET":
        return render_template("play.html", gamedata=loads(details), players=players)

    return redirect(url_for("question", id=request.form.get('id')))


@app.route("/question", methods=['GET', 'POST'])
def question():
    data = loads(player_db.retrieve_dataset('first'))
    players = player_db.retrieve_score()
    question_id = request.args['id']
    display_question = None
    for item in data:
        for sub in data[item]:
            if sub['question_id'] == question_id:
                display_question = sub['question']
                print(sub['answer'])

    if request.method == "GET":
        return render_template("question.html", question=display_question, players=players)

    return redirect(url_for("tally",
                            status=request.form.get('status'),
                            player=request.form.get('player')))


@app.route("/tally", methods=['GET'])
def tally():
    status = request.args['status']
    player = request.args['player']

    return {"player": player, "status": status}
