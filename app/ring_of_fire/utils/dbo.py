import sqlite3


class DBOperations:

    def __init__(self, db_file):

        self.db_file = db_file

        self.conn = None

        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
        except sqlite3.Error as error:
            print(error)

    def create(self):

        sql_create_players = """CREATE TABLE IF NOT EXISTS players(
        id INTEGER,
        name VARCHAR)"""

        sql_create_rules = """CREATE TABLE IF NOT EXISTS rules(
        id INTEGER,
        rule VARCHAR)"""

        sql_create_partners = """CREATE TABLE IF NOT EXISTS partners(
        id INTEGER,
        partner VARCHAR)"""

        sql_empty_players = """DELETE FROM players"""

        sql_empty_rules = """DELETE FROM rules"""

        sql_empty_partners = """DELETE FROM partners"""

        actions = [sql_create_players, sql_create_rules,
                   sql_empty_players, sql_empty_rules,
                   sql_create_partners, sql_empty_partners]

        cur = self.conn.cursor()
        for action in actions:
            cur.execute(action)

        self.conn.commit()

    def insert_player(self, player_id, name):

        sql_insert = """INSERT INTO players (id, name) VALUES (?, ?)"""

        cur = self.conn.cursor()
        cur.execute(sql_insert, [player_id, name])
        self.conn.commit()

        return cur.lastrowid

    def insert_rule(self, player_id, rule):

        sql_insert = """INSERT INTO rules (id, rule) VALUES (?, ?)"""

        cur = self.conn.cursor()
        cur.execute(sql_insert, [player_id, rule])
        self.conn.commit()

        return cur.lastrowid

    def insert_partner(self, player_id, partner):

        sql_insert = """INSERT INTO partners (id, partner) VALUES (?, ?)"""

        cur = self.conn.cursor()
        cur.execute(sql_insert, [player_id, partner])
        self.conn.commit()

        return cur.lastrowid

    def retrieve_player(self, current_player):

        cur = self.conn.cursor()
        sql_select = """SELECT id, name FROM players WHERE players.id = ?"""
        cur.execute(sql_select, [current_player])

        name = cur.fetchone()

        try:
            return name
        except IndexError:
            return "EMPTY DB"

    def all_players(self):

        cur = self.conn.cursor()
        sql_select = """SELECT name FROM players"""
        cur.execute(sql_select)

        players = cur.fetchall()

        try:
            return players
        except IndexError:
            return "EMPTY DB"

    def retrieve_rules(self):

        cur = self.conn.cursor()
        sql_select = """SELECT name, rule FROM players INNER JOIN rules ON rules.id = players.id"""
        cur.execute(sql_select)

        rules = cur.fetchall()

        try:
            return rules
        except IndexError:
            return "EMPTY DB"

    def retrieve_partners(self):

        cur = self.conn.cursor()
        sql_select = """SELECT name, partner FROM players INNER JOIN partners ON partners.id = players.id"""
        cur.execute(sql_select)

        rules = cur.fetchall()

        try:
            return rules
        except IndexError:
            return "EMPTY DB"
