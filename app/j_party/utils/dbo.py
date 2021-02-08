import sqlite3


class JPartyOperations:

    def __init__(self, db_file):

        self.db_file = db_file

        self.conn = None

        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
        except sqlite3.Error as error:
            print(error)

    def select_all(self, show_num, _round):

        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        sql_select = """SELECT * FROM data WHERE data.show_number = ? AND round = ?"""
        cur.execute(sql_select, [str(show_num), str(_round)])

        data = cur.fetchall()

        return data

    def show_numbers(self):

        self.conn.row_factory = None
        cur = self.conn.cursor()
        select = """SELECT DISTINCT show_number FROM data"""
        cur.execute(select)

        data = cur.fetchall()

        show_num = list()
        for item in data:
            show_num.append(item[0])

        return show_num


class PlayerOperations:

    def __init__(self, db_file):

        self.db_file = db_file

        self.conn = None

        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
        except sqlite3.Error as error:
            print(error)

    def create(self):

        sql_create_players = """CREATE TABLE IF NOT EXISTS players(
        name TEXT,
        score INTEGER)"""

        sql_empty_players = """DELETE FROM players"""

        sql_create_dataset = """CREATE TABLE IF NOT EXISTS dataset(
        round TEXT,
        data TEXT)"""

        sql_empty_dataset = """DELETE FROM dataset"""

        sql_create_round = """CREATE TABLE IF NOT EXISTS round(
        round TEXT)"""

        sql_empty_round = """DELETE FROM round"""

        actions = [sql_create_players, sql_empty_players,
                   sql_create_dataset, sql_empty_dataset,
                   sql_create_round, sql_empty_round]

        cur = self.conn.cursor()
        for action in actions:
            cur.execute(action)

        self.conn.commit()

    def insert_player(self, name):

        sql_insert = """INSERT INTO players (name, score) VALUES (?, 0)"""

        cur = self.conn.cursor()
        cur.execute(sql_insert, [name])
        self.conn.commit()

        return cur.lastrowid

    def update_score(self, name, score):

        sql_update = """UPDATE players SET score=? WHERE name=?"""

        cur = self.conn.cursor()
        cur.execute(sql_update, [score, name])
        self.conn.commit()

        return cur.lastrowid

    def retrieve_players(self):

        sql_select = """SELECT * FROM players"""

        cur = self.conn.cursor()
        cur.execute(sql_select)

        name = cur.fetchall()

        try:
            return name
        except IndexError:
            return "EMPTY DB"

    def retrieve_player_score(self, player):
        sql_select = """SELECT score FROM players WHERE name=?"""

        cur = self.conn.cursor()
        cur.execute(sql_select, [player])

        name = cur.fetchone()

        try:
            return name[0]
        except IndexError:
            return "EMPTY DB"

    def insert_game_data(self, game_round, dataset):

        sql_insert = """INSERT INTO dataset (round, data) VALUES (?, ?)"""

        cur = self.conn.cursor()
        cur.execute(sql_insert, [game_round, dataset])
        self.conn.commit()

        return cur.lastrowid

    def update_dataset(self, game_round, dataset):
        sql_update = """UPDATE dataset SET data=? WHERE round=?"""

        cur = self.conn.cursor()
        cur.execute(sql_update, [dataset, game_round])
        self.conn.commit()

        return cur.lastrowid

    def retrieve_dataset(self, game_round):

        sql_select = """SELECT data FROM dataset WHERE round=?"""

        cur = self.conn.cursor()
        cur.execute(sql_select, [game_round])

        data = cur.fetchone()

        try:
            return data[0]
        except IndexError:
            return "EMPTY DB"

    def insert_round(self, game_round):

        sql_insert = """INSERT INTO round (round) VALUES (?)"""

        cur = self.conn.cursor()
        cur.execute(sql_insert, [game_round])
        self.conn.commit()

        return cur.lastrowid

    def update_round(self, game_round):
        sql_update = """UPDATE round SET round=?"""

        cur = self.conn.cursor()
        cur.execute(sql_update, [game_round])
        self.conn.commit()

        return cur.lastrowid

    def retrieve_round(self):

        sql_select = """SELECT round FROM round"""

        cur = self.conn.cursor()
        cur.execute(sql_select)

        data = cur.fetchone()

        try:
            return data[0]
        except IndexError:
            return "EMPTY DB"
