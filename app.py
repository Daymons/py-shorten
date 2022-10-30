import flask, random, sqlite3
app = flask.Flask(__name__)
rstring = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(8))

# Configuration strings
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
            k = ''.join(''.join(n) for n in i)
            return flask.redirect(k)
            
@app.route("/shorten/", methods = ["POST"])
def handler():
    link = flask.request.form.get('url')
    con = sqlite3.connect("static/short.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO links VALUES (?, ?)", (rstring, link))
    con.commit()
    return f"{baseurl}/{rstring}"

if __name__ == "__main__":
    app.run()