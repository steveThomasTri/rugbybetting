from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB = "betting.db"

def get_db(DB):
    try:
        db = sqlite3.connect(DB)
        return db
    except sqlite3.Error as e:
        print(f"Error opening database: {e}")
        return None

@app.route("/")
def index():
    db = get_db(DB)
    players = db.execute("SELECT * FROM Players").fetchall()
    print(players)

    totals = db.execute("""
        SELECT Players.ID, Name, Bank,
               COALESCE(SUM(AmountWon),0) as result,
               Bank + COALESCE(SUM(AmountWon),0) as total
        FROM Players
        LEFT JOIN Transactions ON Players.ID = Transactions.PlayerID
        GROUP BY Players.ID
        ORDER BY total DESC
    """).fetchall()
    return render_template("index.html", players=totals)


@app.route("/player/<int:id>")
def player(id):
    db = get_db()
    player = db.execute("SELECT * FROM Players WHERE ID = ?", (id,)).fetchone()

    transactions = db.execute(
        "SELECT * FROM Transactions WHERE PlayerID = ?", (id,)
    ).fetchall()

    return render_template("player.html", player=player, transactions=transactions)


@app.route("/transactions")
def transactions():
    db = get_db(DB)
    data = db.execute("""
        SELECT Transactions.*, Players.Name
        FROM Transactions
        JOIN Players ON Players.ID = Transactions.PlayerID
    """).fetchall()
    print(data)
    return render_template("transactions.html", transactions=data)


@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    db = get_db()

    if request.method == "POST":
        player_id = request.form["player_id"]
        team = request.form["team"]
        bettype = request.form["bettype"]
        description = request.form["description"]
        odds = int(request.form["odds"])
        amount = float(request.form["amount"])
        status = request.form["status"]

        db.execute("""
            INSERT INTO Transactions
            (PlayerID, Team, BetType, Description, Odds, AmountBet, Status, AmountWon)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (player_id, team, bettype, description, odds, amount, status))

        db.commit()
        return redirect(url_for("transactions"))

    players = db.execute("SELECT * FROM Players").fetchall()
    return render_template("add_transaction.html", players=players)


@app.route("/review", methods=["GET", "POST"])
def review():
    db = get_db(DB)

    if request.method == "POST":
        t_id = request.form["id"]
        status = request.form["status"]
        odds = float(request.form["odds"])
        amount = float(request.form["amount"])

        if status == "Win":
            if odds > 0:
                won = round(odds * amount / 100, 2)
            else:
                won = round(amount * (100 / abs(odds)), 2)

        elif status == "Loss":
            won = -amount
        else:
            return redirect(url_for("review"))

        db.execute("""
            UPDATE Transactions
            SET Status = ?, AmountWon = ?
            WHERE ID = ?
        """, (status, won, t_id))

        db.commit()
        return redirect(url_for("review"))

    pending = db.execute("""
        SELECT Transactions.*, Players.Name
        FROM Transactions
        JOIN Players ON Players.ID = Transactions.PlayerID
        WHERE Status = 'Pending'
    """).fetchall()

    return render_template("review.html", transactions=pending)


@app.route("/leaderboard")
def leaderboard():
    db = get_db()
    data = db.execute("""
        SELECT Players.Name, SUM(AmountWon) as total
        FROM Transactions
        JOIN Players ON Players.ID = Transactions.PlayerID
        GROUP BY PlayerID
        ORDER BY total DESC
    """).fetchall()

    return render_template("leaderboard.html", players=data)


if __name__ == "__main__":
    app.run(debug=True)