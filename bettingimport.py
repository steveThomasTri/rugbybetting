import sqlite3

con = sqlite3.connect('betting.db')
f = open('betting.sql','r')
str = f.read()
con.executescript(str)