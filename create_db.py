import os
import sqlite3
from os.path import exists


DB_NAME = 'DataBase.sqlite'


def create_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    with open('create_db.sql', 'r') as f:
        text = f.read()
    cur.executescript(text)
    cur.close()
    con.close()


if __name__ == '__main__':
    create_db()
