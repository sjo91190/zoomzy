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

		sql_create = """CREATE TABLE IF NOT EXISTS players(
		id INTEGER,
		name VARCHAR)"""

		sql_empty = """DELETE FROM players"""

		sql_reset = """ALTER"""

		cur = self.conn.cursor()
		cur.execute(sql_create)
		cur.execute(sql_empty)
		self.conn.commit()

	def insert(self, player_id, name):

		sql_insert = """INSERT INTO players (id, name) VALUES (?, ?)"""

		cur = self.conn.cursor()
		cur.execute(sql_insert, [player_id, name])
		self.conn.commit()

		return cur.lastrowid

	def retrieve(self, current_player):

		cur = self.conn.cursor()
		sql_select = """SELECT id, name FROM players WHERE players.id = ?"""
		cur.execute(sql_select, [current_player])

		name = cur.fetchone()

		try:
			return name
		except IndexError:
			return "EMPTY DB"
