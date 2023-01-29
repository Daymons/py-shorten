import flask, sqlite3, random, validators
app = flask.Flask(__name__)
app.secret_key = "[qPH5,T¡3?m6c4HP}JG2hYf8xkMyOVq]xgch1PKMb02BHpV6,U1?abd!L0qr¡kZH0wjOd1CQW¿NDQd2S?WxFYhzd8gVOdpIjFYB9]zHZM¿¿y4BGDaljLpf6xt4.nz{,:"

base_url = "https://your-url-here.net/"
short_code = ''.join(random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890") for i in range(8))

@app.route("/")
def main():
    return flask.render_template("index.html")

@app.route("/shorten", methods = ["POST"])
@app.route("/shorten/", methods = ["POST"])
def shorten():
    # Connect to the database and initialize the cursor.
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()

    # Get the HTML link and search for the link in the database.
    html_link = flask.request.form.get("link")
    if validators.url(html_link):
        db_link = cur.execute("SELECT short FROM links WHERE long = ?", (html_link,)).fetchone()

        # Search the database for the link. If it exists, return the already existing short code. This prevents the database being flooded with different short codes for the same long link. 
        # If it doesn't exist, create a new code and return it.
        if db_link == None:
            cur.execute("INSERT INTO links VALUES (?, ?)", (html_link, short_code))
            con.commit()
            flask.flash("Your link is " + base_url + short_code)
            return flask.redirect("/")
        else:
            flask.flash("Your link is " + base_url + ''.join(db_link))
            return flask.redirect("/")
    else:
        flask.flash("The URL you inputed is not valid.", "error")
        return flask.redirect("/")

@app.route("/<code>")
def redirect(code):
    cur = sqlite3.connect("sqlite3.db").cursor()
    db_link = cur.execute("SELECT long FROM links WHERE short = ?", (code,)).fetchone()

    if db_link == None:
        flask.flash("The entered URL does not exist.", "error")
        return flask.redirect("/")
    else:
        return flask.redirect(''.join(db_link))

if __name__ == '__main__':
    import waitress
    waitress.serve(app, host="0.0.0.0", port="8080")
