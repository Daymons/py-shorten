import flask, random, sqlite3, validators
app = flask.Flask(__name__)
baseurl = "https://s.example.com"

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/<url>/")
def linkredirecter(url):
    assert url == flask.request.view_args['url']
    con = sqlite3.connect("static/short.db")
    cur = con.cursor()
    if url != '':
        cur.execute("SELECT * FROM links WHERE short = ?", (url,))
        a = cur.fetchall()
        if len(a) == 0:
            return flask.render_template("404.html")
        else:
            cur.execute("SELECT original FROM links WHERE short = ?", (url,))
            i = cur.fetchall()
            original_link = ''.join(''.join(n) for n in i)
            return flask.redirect(original_link)
     
@app.route("/shorten/", methods = ["POST", "GET"])
def handler():
    link = flask.request.form.get('url')
    rstring = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(8))
    con = sqlite3.connect('static/short.db')
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    originals = cur.execute('SELECT original FROM links').fetchall()
    if link in originals:
        cur.execute('SELECT short FROM links WHERE original = (?)', (link,))
        res = cur.fetchall()
        short = ''.join(res)
        return f"{baseurl}/{short}"
    else:
        rstring = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(8))
        cur.execute(f"INSERT INTO links VALUES (?, ?)", (rstring, link))
        con.commit()
        return f"{baseurl}/{rstring}"

@app.route("/api", methods=["POST", "GET"])
def apihandler():
    link = flask.request.args.get('url')
    if validators.url(link):
        rstring = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(8))
        con = sqlite3.connect('static/short.db')
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()
        originals = cur.execute('SELECT original FROM links').fetchall()
        if link in originals:
            cur.execute('SELECT short FROM links WHERE original = (?)', (link,))
            res = cur.fetchall()
            short = ''.join(res)
            return f"{baseurl}/{short}"
        else:
            rstring = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(8))
            cur.execute(f"INSERT INTO links VALUES (?, ?)", (rstring, link))
            con.commit()
            return f"{baseurl}/{rstring}"
    else:
        return "Your URL is malformed. Perhaps you forgot to add 'https://' at the beggining?"

if __name__ == "__main__":
    app.run()
