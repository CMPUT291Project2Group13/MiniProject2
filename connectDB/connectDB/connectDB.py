import sqlite3

c = None
conn = None

def connect(path):
	# -establishes a connection to the database
	# -path is the name of the database
	# -init_file is an sql file with commands to create tables
	global conn,c
	conn = sqlite3.connect(path)
	                 ###conn.row_factory = sqlite3.Row #need it?????? - works without it too
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys = ON; ')
	conn.commit()
	return c,conn


def disconnect():
	conn.close()

