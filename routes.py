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
    cur.execute('''SELECT name, details, image, developerid, categoryid FROM
                Games WHERE name=?''', (game,))
    results = cur.fetchone()

    cur.execute("SELECT name FROM Developer WHERE id=?", (results[3],))
    developer = cur.fetchone()

    cur.execute("SELECT name, details FROM Category WHERE id=?", (results[4],))
    category = cur.fetchone()

    cur.execute('''SELECT name from Console INNER JOIN GamesConsole ON
                Console.id=GamesConsole.cid
                WHERE gid=(select id FROM Games
                           WHERE name=?)''', (game,))
    console = cur.fetchone()
    cat = cur.fetchone()
    return render_template("show_games.html", page_title='{}'.format(game),
                           results=results, category=category,
                           developer=developer, cat=cat, console=console)


@app.route('/developer')
def circumnavigation():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Developer")
    results = cur.fetchall()
    return render_template("developer.html",
                           page_title="RETRO DEVELOPERS", results=results)


@app.route('/developer/<developer>')
def developers(developer):
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT name, details, image FROM Developer WHERE name=?",
                (developer,))
    results = cur.fetchone()
    return render_template("show_developer.html",
                           page_title='{}'.format(developer), results=results)


@app.route('/contact')
def contact():
    return render_template("contact.html", page_title="CONTACT US")


if __name__ == "__main__":
    app.run(debug=True, port=1111)
