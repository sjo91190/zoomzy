from flask import request, render_template, redirect, url_for
from app.ring_of_fire.utils.actions import card_actions
from app.ring_of_fire.utils.tools import random_card, shuffle, top_pop, next_player
from app.ring_of_fire import ring_of_fire
from app.ring_of_fire.forms import PlayerCountForm, PlayerNameForm, CardActionsForm
from app import db
from app.models import ROFRules, ROFPartners, ROFPlayers

cards = list()
player_config = dict()


@ring_of_fire.route("/rof_home", methods=['GET', 'POST'])
def home():
    form = PlayerCountForm()
    if len(cards) == 0:
        shuffle(cards)

    if request.method == "GET":
        db.drop_all()
        db.create_all()
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
            player = ROFPlayers(player_id=i, name=form.data.get(f"player{i}"))
            db.session.add(player)
            db.session.commit()

        return redirect(url_for("ring_of_fire.play_rof", index=0))


@ring_of_fire.route("/play", methods=['GET', 'POST'])
def play_rof():
    form = CardActionsForm()

    if request.method == "GET":
        card = random_card(cards)

        player_config["INDEX"] = int(request.args["index"])

        player = ROFPlayers.query.filter_by(player_id=player_config["INDEX"]).first()

        prompt = card_actions(card[0], player.name)

        players = ROFPlayers.query.order_by(ROFPlayers.id).all()
        rules = db.session.query(ROFPlayers, ROFRules).filter(ROFRules.player_id == ROFPlayers.player_id).all()
        partners = db.session.query(ROFPlayers, ROFPartners).filter(ROFPartners.player_id == ROFPlayers.player_id).all()

        pop = top_pop(player_config)

        if card[0] == "5":
            player_config["THUMB"] = player.name

        if card[0] == "Q":
            player_config["QUESTION"] = player.name

        return render_template("ring_of_fire/play.html", card=card, name=player.name,
                               prompt=prompt, players=players, rules=rules,
                               thumb=player_config.get("THUMB"), question=player_config.get("QUESTION"),
                               partners=partners, pop=pop, form=form)

    rule = form.custom_rule.data
    if rule:
        insert_rule = ROFRules(player_id=player_config["INDEX"], rule=str(rule))
        db.session.add(insert_rule)
        db.session.commit()

    partner = form.drinking_partner.data
    if partner:
        insert_partner = ROFPartners(player_id=player_config["INDEX"], partner=str(partner))
        db.session.add(insert_partner)
        db.session.commit()

    return redirect(
        url_for(
            "ring_of_fire.play_rof", index=next_player(index=player_config["INDEX"],
                                                       count=player_config["COUNT"])
        )
    )
