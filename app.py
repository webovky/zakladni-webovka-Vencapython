from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
""" secret_key se generuje pomoc os.urandom(počet znaku davej 24)
    ale obecně je to prostě velké náhodné číslo
    proměnnou secret_key nikdy nesdílím v depozitáři tak jako teď
"""

app.secret_key = b'os.urandom(24)'


@app.route("/")
def index():
    return render_template("base.html.j2")


@app.route("/1/", methods=["GET"])
def jedna():
    try:
        x = request.args.get("x")
        y = request.args.get("y")
        soucet = int(x) + int(y)
    except TypeError:
        soucet = None
    except ValueError:
        soucet = "Nedělej si srandu!!!"

    slovo = request.args.get('slovo')
    if slovo:
        session['slovo'] = slovo

    return render_template("1.html.j2", soucet=soucet)


@app.route("/1/", methods=["POST"])
def jedna_post():

    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    print("POST:", jmeno, heslo)

    return redirect(url_for("jedna"))


@app.route("/2/")
def dva():
    return render_template("2.html.j2")


@app.route("/3/")
def tri():
    if "user" in session:
        return render_template("3.html.j2")
    else:
        flash(f"Pro zobrazení této stránky ({request.path}) je nutné se přihlásit!", "err")
        return redirect(url_for("login", next=request.path))

@app.route("/Login/", methods=["GET"])
def login():
    if request.method== "GET":
        login=request.args.get("nick")
        passwd= request.args.get("pswd")
        print(login, passwd)
    return render_template("login.html.j2")


@app.route("/Login/", methods=["POST"])
def login_post():
    login= request.form.get("nick")
    passwd= request.form.get("pswd")
    print(login, passwd)
    next= request.args.get("next")
    if login =="venca" and passwd =="1234":
        session["user"]=login
        flash("úspěšně jsi se přihlasil", "pass")
        if next:
            return redirect(next)
    else:
        flash("neplatné přihlašovací údaje", "err")
    if next:
        return redirect(url_for("login",next=next))
    else:
        return redirect(url_for("login"))

@app.route("/Logout/")
def logout():
    session.pop("user", None)
    flash("právě jsi se odhlásil", "pass")
    return redirect (url_for("login"))