from app import db


class ROFPlayers(db.Model):
    __tablename__ = "players"
    __bind_key__ = "ring_of_fire"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    name = db.Column(db.String(64))

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name


class ROFRules(db.Model):
    __tablename__ = "rules"
    __bind_key__ = "ring_of_fire"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    rule = db.Column(db.Text)

    def __init__(self, player_id, rule):
        self.player_id = player_id
        self.rule = rule


class ROFPartners(db.Model):
    __tablename__ = "partners"
    __bind_key__ = "ring_of_fire"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    partner = db.Column(db.String(64))

    def __init__(self, player_id, partner):
        self.player_id = player_id
        self.partner = partner
