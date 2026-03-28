import sqlite3
import os
import questionary
import time
import pandas as pd

# Player represents a player in the betting game.
class Player:
    def __init__(self, id, name, bets_placed, success_rate, bank):
        self.id = id
        self.name = name
        self.bets_placed = bets_placed
        self.success_rate = success_rate
        self.bank = bank

# Initializes the database and creates the tables.
def init_db(filepath):
    try:
        db = sqlite3.connect(filepath)
        return db
    except sqlite3.Error as e:
        print(f"Error opening database: {e}")
        return None

# Creates the Players and Transactions tables.
def create_tables(db):
    players_table = '''CREATE TABLE IF NOT EXISTS Players (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        BetsPlaced INTEGER,
                        SuccessRate REAL,
                        Bank REAL
                    );'''

    transactions_table = '''CREATE TABLE IF NOT EXISTS Transactions (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            PlayerID INTEGER,
                            Team TEXT,
                            BetType TEXT,
                            Description TEXT,
                            Odds INTEGER,
                            AmountBet REAL,
                            Status TEXT,
                            AmountWon REAL,
                            FOREIGN KEY(PlayerID) REFERENCES Players(ID)
                        );'''

    try:
        db.execute(players_table)
        db.execute(transactions_table)
        db.commit()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# Seeds the database with initial player data.
def seed_players(db, filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return

    with open(filename, "r") as file:
        for line in file:
            name = line.strip()
            try:
                db.execute("INSERT INTO Players(Name, BetsPlaced, SuccessRate, Bank) VALUES (?, ?, ?, ?)", 
                           (name, 0, 0.0, 50.0))
                db.commit()
            except sqlite3.Error as e:
                print(f"Error inserting player {name}: {e}")

# Function to view the current totals of players.
def view_current_totals(db):
    try:
        #temp table
        db.execute("DROP TABLE IF EXISTS Total_Result")
        db.execute("CREATE TEMP TABLE Total_Result AS SELECT Players.ID, Name, Bank, round(SUM(AmountWon),2) as Resul FROM Players INNER JOIN Transactions on Transactions.PlayerID = Players.ID GROUP BY PlayerID")
        db.commit()
        db.execute("ALTER TABLE Total_Result add column total real as (Bank + Resul)")
        db.commit()
        cursor = db.execute("SELECT * FROM Total_Result ORDER by total DESC")
        print("Total Results\n--------------------------------")
        for row in cursor:
            if not row[1] == "ADAM":
                print(f"Player: {row[1]}, Bank: ${row[4]:.2f}")
    except sqlite3.Error as e:
        print(f"Error fetching totals: {e}")

# Function to view a single player.
def view_one_player(db, name):
    try:
        cursor = db.execute("SELECT * FROM Players WHERE Name = ?", (name,))
        row = cursor.fetchone()
        if row:
            player = Player(row[0], row[1], row[2], row[3], row[4])
            print(f"Player: {player.name}, Bets Placed: {player.bets_placed}, "
                  f"Success Rate: {player.success_rate:.2f}, Bank: {player.bank:.2f}")
            return player
        else:
            print(f"No player found with the name {name}")
            return None
    except sqlite3.Error as e:
        print(f"Error retrieving player: {e}")
        return None
    
def create_transaction(db):
    try:
        #creat player in name tag as choice
        #questionary.selectf
        nameList = []
        cur = db.execute("SELECT Name FROM Players")
        for row in cur:
            if not row[0] == "ADAM":
                nameList.append(row[0])
        name = questionary.select("Player: ", choices=nameList).ask()
        team = questionary.text("Team: ").ask()
        bettype = questionary.text("Bet Type: ").ask()
        description = questionary.text("Bet Description: ").ask()
        odds = questionary.text("Odds: ").ask()
        amountbet = questionary.text("Betting Amount: ").ask()
        status = questionary.select("Status: ",choices=["Win","Loss","Pending"]).ask()

        cursor = db.execute("SELECT ID FROM Players WHERE Name = ?", (name,))
        playerid = cursor.fetchone()
        time.sleep(1)
        print(playerid[0])

        if playerid[0] > 0:
            try:
                db.execute("INSERT INTO Transactions(PlayerID, Team, BetType, Description, Odds, AmountBet, Status, AmountWon) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                           (playerid[0], team, bettype, description, odds, amountbet, status, 0))
                db.commit()
            except sqlite3.Error as e:
                print(f"Error inserting Transaction: {e}")
        elif playerid[0] == None:
            print("Sorry, no person was found!")

    except:
        pass

def view_transaction(db):
    try:
        cursor = db.execute("SELECT * FROM Transactions")

        #LOOKING TO PUT LOGIC FOR 0 TRANSACTIONS BEFORE GOING TO THE FOR LOOP
        transactionList = 0

        for row in cursor:
            print(f"Transaction: {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]:.2f}, {row[7]}, {row[8]:.2f}")
            transactionList += 1
        if transactionList == 0:
            print("No Transactions Present")
    except sqlite3.Error as e:
        print(f"Error fetching totals: {e}")

def review_pending_transactions(db):
    try:
        cursor = db.execute("SELECT * FROM Transactions WHERE Status = 'Pending'")
        pending_transactions = cursor.fetchall()

        if len(pending_transactions) == 0:
            print("There are no Pending Transactions")
        else:
            for t in pending_transactions:
                status = questionary.select(f"What would you like to do with the following transaction: \n Team: {t[2]}\n Bet Type:{t[3]}\n Description: {t[4]}\n Odds: {t[5]}",choices=["Win","Loss","No Change"]).ask()

                if status == "Win":
                    print(f"Odds: {t[5]}")
                    print(f"Amount Bet: {t[6]}")

                    if t[5] > 0:
                        amountwon = round(t[5] * t[6] / 100 , 2)
                        db.execute(f"UPDATE Transactions SET AmountWon = {amountwon}, Status = 'Win' WHERE ID = {t[0]}")
                        db.commit()
                        print(f"Amount won: {amountwon}")

                    elif t[5] < 0:
                        amountwon = round(1000 * t[6] / abs(t[5]) / 10 , 2)
                        db.execute(f"UPDATE Transactions SET AmountWon = {amountwon}, Status = 'Win' WHERE ID = {t[0]}")
                        db.commit()
                        print(f"Amount won: {amountwon}")
                elif status == "Loss":
                    print(f"Odds: {t[5]}")
                    print(f"Amount Bet: {t[6]}")
                    print(f"Amount Lost: {-t[6]}")
                    db.execute(f"UPDATE Transactions SET AmountWon = {-t[6]}, Status = 'Loss' WHERE ID = {t[0]}")
                    db.commit()
                elif status == "No Change":
                    pass

    except sqlite3.Error as e:
        print(e)
def groupby_transaction(db):
    cursor = db.execute("SELECT PlayerID,Name, SUM(AmountWon) FROM Transactions INNER JOIN Players on Transactions.PlayerID = Players.ID GROUP BY PlayerID ORDER BY SUM(AmountWon) DESC")
    try:
        for row in cursor:
            print(f"{row[1]}, ${row[2]:.2f}")
    except sqlite3.Error as e:
        print(f"Error fetching totals: {e}")


def export_database():
    try:
        conn = sqlite3.connect("betting.db")
        with open("betting.sql", 'w') as f:
            for line in conn.iterdump():
                f.write(line + '\n')
        conn.close()
        print(f"Database exported to betting.sql")
    except sqlite3.Error as e:
        print(f"Error exporting database: {e}")


def main():
    if os.path.exists("betting.db"):
        db = init_db("betting.db")
    else:
        db = init_db("betting.db")
        create_tables(db)
        seed_players(db, "hollywood/players_seed.txt")

    if db:
        # Ask for player name
        over = False
        while over == False:
            userDecision = questionary.select(
            "Make a Selection?",
            choices=[
                'Select One',
                'Show All',
                'Insert Transaction',
                'View Transaction',
                'Review Pending Transactions',
                'Export Database',
                'Group By Transaction',
                'Exit'
            ]).ask()
            match userDecision:
                case "Select One":
                    first = input("Who do you want to check? ")
                    # Fetch player details
                    player = view_one_player(db, first)
                    if player is None:
                        print("No player found.")
                case "Show All":
                    view_current_totals(db)
                case "Insert Transaction":
                    create_transaction(db)
                case "View Transaction":
                    view_transaction(db)
                case "Review Pending Transactions":
                    review_pending_transactions(db)
                case "Export Database":
                    export_database()
                case "Group By Transaction":
                    groupby_transaction(db)
                case "Exit":
                    over = True
                case default:
                    pass

if __name__ == "__main__":
    main()
