from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import time

DB = "betting.db"
db = sqlite3.connect(DB)


for player in [[3,50],[7,40],[5,30],[6,30],[1,30]]:
    db.execute("""
            UPDATE Players
            SET Bank = Bank + ?
            WHERE ID = ?
        """, (player[1], player[0]))

db.commit()