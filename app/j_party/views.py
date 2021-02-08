# import random
# from uuid import uuid4
# from json import loads, dumps
# from pathlib import Path
# from os import urandom, makedirs, path
# from flask import Flask, request, render_template, redirect, url_for
# from app.j_party.utils.dbo import JPartyOperations, PlayerOperations
#
# from app.j_party import j_party
#
# pkg_root = path.split(__file__)[0]
#
# data_path = Path(pkg_root, "database")
#
# data_db_path = Path(data_path, "jpartydata.db")
# data_db = JPartyOperations(data_db_path)
#
# player_path = Path(pkg_root, "data")
# if not Path.is_dir(player_path):
#     makedirs(player_path)
#
# player_db_path = Path(player_path, "players.db")
# player_db = PlayerOperations(player_db_path)
#
# rounds = ["first", "second", "final"]
#
#
# def play_set():
#     show_num = data_db.show_numbers()
#     _set = random.choice(show_num)
#
#     def get_data(_round):
#
#         _game = dict()
#         game = dict()
#
#         round_data = data_db.select_all(_set, _round)
#
#         category = list(set(_['category'] for _ in round_data))
#
#         for cat in category:
#             _game[cat] = list()
#             for data in round_data:
#                 if data['category'] == cat:
#                     _game[cat].append(dict(value=data['value'],
#                                            question=data['question'],
#                                            answer=data['answer'],
#                                            question_id=str(uuid4()),
#                                            active=True))
#
#             if _round == "first" or _round == "second":
#                 game[cat] = sorted(_game[cat], key=lambda v: int(v['value'].strip("$").replace(",", "")))
#             else:
#                 game = _game
#
#         return game
#
#     for item in rounds:
#         player_db.insert_game_data(item, str(dumps(get_data(item))))
#
#
# @j_party.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == "GET":
#         player_db.create()
#         player_db.insert_round("first")
#         play_set()
#
#         return render_template("assign.html")
#
#     if request.method == "POST":
#         for i in range(3):
#             player_db.insert_player(name=request.form.get(f"player{i}"))
#
#     return redirect(url_for("jparty"))
#
#
# @j_party.route("/play", methods=['GET', 'POST'])
# def jparty():
#     current_round = player_db.retrieve_round()
#     details = loads(player_db.retrieve_dataset(current_round))
#     players = player_db.retrieve_players()
#
#     next_round = list()
#     for item in details:
#         for active in details[item]:
#             next_round.append(active['active'])
#
#     if True in next_round:
#         round_over = False
#     else:
#         round_over = True
#
#     if request.method == "GET":
#
#         return render_template("play.html",
#                                gamedata=details,
#                                players=players,
#                                current_round=current_round,
#                                round_over=round_over)
#
#     if round_over and request.method == "POST":
#         if current_round == "first":
#             player_db.update_round("second")
#             return redirect(url_for("jparty"))
#
#         if current_round == "second":
#             player_db.update_round("final")
#             return redirect(url_for("jparty"))
#
#         if current_round == "final":
#             return redirect(url_for("index"))
#
#     if request.method == "POST" and current_round == "final":
#         wagers = dict()
#         for player in players:
#             wagers[player[0]] = int(request.form.get(player[0]))
#
#         return redirect(url_for("question", id=request.form.get('id'), wager=dumps(wagers)))
#
#     return redirect(url_for("question", id=request.form.get('id')))
#
#
# @j_party.route("/question", methods=['GET', 'POST'])
# def question():
#
#     display_question = None
#     question_points = None
#
#     current_round = player_db.retrieve_round()
#     data = loads(player_db.retrieve_dataset(current_round))
#     players = player_db.retrieve_players()
#     question_id = request.args['id']
#
#     has_wager = False
#     if current_round == "final":
#         has_wager = True
#
#     answer = None
#     for item in data:
#         for sub in data[item]:
#             if sub['question_id'] == question_id:
#                 display_question = sub['question']
#                 question_points = sub['value'].strip("$")
#                 sub['active'] = False
#                 player_db.update_dataset(current_round, dumps(data))
#                 answer = sub['answer']
#
#     if request.method == "GET":
#         print("\n")
#         print("*--------------------*")
#         print(answer)
#         print("*--------------------*")
#         print("\n")
#         return render_template("question.html", question=display_question, players=players, has_wager=has_wager)
#
#     if current_round == "first" or current_round == "second":
#         return redirect(url_for("tally_score",
#                                 id=question_id,
#                                 status=request.form.get('status'),
#                                 player=request.form.get('player'),
#                                 value=question_points))
#
#     wager = loads(request.args['wager'])
#     status = dict()
#     for player in players:
#         status[player[0]] = request.form.get(player[0])
#
#     return redirect(url_for("end", wager=dumps(wager), status=dumps(status)))
#
#
# @j_party.route("/tally", methods=['GET'])
# def tally_score():
#
#     player = request.args['player']
#     status = request.args['status']
#     value = int(request.args['value'].replace(",", ""))
#
#     score = int(player_db.retrieve_player_score(player))
#
#     if status == "correct":
#         score += value
#     else:
#         score -= value
#
#     player_db.update_score(name=player, score=score)
#
#     if status == "correct":
#         return redirect(url_for("jparty"))
#
#     return redirect(url_for("question", id=request.args['id']))
#
#
# @j_party.route("/end", methods=['GET', 'POST'])
# def end():
#     players = player_db.retrieve_players()
#     wager = loads(request.args['wager'])
#     status = loads(request.args['status'])
#
#     print(wager)
#     print(status)
#
#     for player in players:
#         score = int(player_db.retrieve_player_score(player[0]))
#         if status[player[0]] == "correct":
#             score += wager[player[0]]
#         else:
#             score -= wager[player[0]]
#
#         player_db.update_score(player[0], score)
#
#     final_scores = sorted(player_db.retrieve_players(), key=lambda v: v[1], reverse=True)
#     winner = final_scores[0][0]
#     return render_template("end.html", players=final_scores, winner=winner)
