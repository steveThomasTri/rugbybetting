from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import time

DB = "betting.db"
db = sqlite3.connect(DB)

#haz 1
#henkel 3
#blaze 5
#enzo 6
#trif 7
for player in [[1,40],[3,40],[5,50],[6,50],[7,40]]:
    db.execute("""
            UPDATE Players
            SET Bank = Bank + ?
            WHERE ID = ?
        """, (player[1], player[0]))

db.commit()