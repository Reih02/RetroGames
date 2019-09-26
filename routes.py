# tells python to use flask module and other things I need such as sqlite3 for
# database integration
from flask import Flask, render_template
import sqlite3
from forms import SearchForm

app = Flask(__name__)

# defines token to protect site from XSS attacks
app.config['SECRET_KEY'] = 'secrettoken123456789'


# injects the search form (flask-wtf) into all of my pages
@app.context_processor
def inject_search():
    searchform = SearchForm()
    return dict(searchform=searchform)


# returns a search result for a search relevant to each table seperately
@app.route('/gsearch', methods=['POST'])
def gsearch():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    form = SearchForm()
    cur.execute("SELECT * FROM Games WHERE name LIKE ?",
                ("%"+form.query.data+"%",))
    game = cur.fetchall()
    return render_template('gsearch.html', title='Search', game=game)


@app.route('/dsearch', methods=['POST'])
def dsearch():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    form = SearchForm()
    cur.execute("SELECT * FROM Developer WHERE name LIKE ?",
                ("%"+form.query.data+"%",))
    developer = cur.fetchall()
    return render_template('dsearch.html', title='Search', developer=developer)


@app.route('/csearch', methods=['POST'])
def csearch():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    form = SearchForm()
    cur.execute("SELECT * FROM Console WHERE name LIKE ?",
                ("%"+form.query.data+"%",))
    console = cur.fetchall()
    return render_template('csearch.html', title='Search', console=console)


# defines base url as home page and tells flask what page to bring up for this
# route
@app.route('/')
def home():
    return render_template("home.html", page_title="WELCOME TO RETRO GAMES")


# route for my first non-home page, games. This page is told to select all
# data from the database table named Games and displays this on the list_games
# page.
@app.route('/games')
def navigation():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games ORDER BY name ASC")
    results = cur.fetchall()
    return render_template("list_games.html", page_title="RETRO GAMES",
                           results=results)


# this route is for the show_games page, where details are shown on the
# selected game. It has 4 different queries with the database to do a
# bring up different data from the database relating to the Games, Developer,
# Category, and GamesConsole tables.
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


# this route selects all data in the Developer table in the database to display
# on developer.html page.
@app.route('/developer')
def circumnavigation():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Developer ORDER BY name ASC")
    results = cur.fetchall()
    return render_template("list_developer.html",
                           page_title="RETRO DEVELOPERS", results=results)


# on the show_developer page, this route displays the name, details, and image
# from the Developer table
@app.route('/developer/<developer>')
def developers(developer):
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT name, details, image FROM Developer WHERE name=?",
                (developer,))
    results = cur.fetchone()
    return render_template("show_developer.html",
                           page_title='{}'.format(developer), results=results)


# brings in all data from the Console table from my database into this route
@app.route('/console')
def circumambulate():
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Console ORDER BY name ASC")
    results = cur.fetchall()
    return render_template("list_console.html", page_title="RETRO CONSOLES",
                           results=results)


# shows more information on each console (name, details, and image from the
# console table in my database)
@app.route('/console/<console>')
def consoles(console):
    conn = sqlite3.connect("retro_games.db")
    cur = conn.cursor()
    cur.execute("SELECT name, details, image FROM Console WHERE name=?",
                (console,))
    results = cur.fetchone()
    return render_template("show_console.html",
                           page_title='{}'.format(console), results=results)


# page with no database interaction, just displays html and css from the
# contact.html page
@app.route('/contact')
def contact():
    return render_template("contact.html", page_title="CONTACT US")

# gives user an error when URL entered doesn't go to a route on the site
@app.errorhandler(404)
def page_not_found(f):
    return render_template('404.html'), 404


# runs site on local port 1111
if __name__ == "__main__":
    app.run(debug=True, port=1111, use_evalex=False)
