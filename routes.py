from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", page_title="WELCOME TO RETRO GAMES")

@app.route('/games')
def navigation():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games;")
    results = cur.fetchall()
    return render_template("list_games.html", page_title="RETRO GAMES",
                           results=results)

@app.route('/games/<game>')
def game(game):
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT name, details, image FROM Games WHERE name='{}'"
                .format(game))
    results = cur.fetchone()
    return render_template("show_games.html", page_title='{}'.format(game),
                       results=results)

@app.route('/contact')
def contact():
    return render_template("contact.html", page_title="CONTACT US")

if __name__ == "__main__":
    app.run(debug=True, port=1111)
