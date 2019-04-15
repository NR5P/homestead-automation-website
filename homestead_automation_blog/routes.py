from flask import render_template, url_for, redirect, flash
from homestead_automation_blog import app, db, bcrypt
from homestead_automation_blog.forms import RegistrationForm, LoginForm
from homestead_automation_blog.models import User, Post

posts = [
    {
        "author" : "Nathan Rigg",
        "title" : "post 1",
        "content" : "here is some reaanndome conetent ui8woafjd siaopf djsaiofp djsaopf sjifo dsjf idsopajfdsiopf ds fdsap j jfi dsoap jfdsoapfjdiso pfdjsaio pj ",
        "date_posted" : "april 20, 2019"
    },
    {
        "author" : "Nathan Rigg",
        "title" : "post 2",
        "content" : "second post content jiofdpsa jfodspa fj fdjiso apfjdiso apj p jdiso pdjiso apjiospa jfsap fop fjisa opjs i odps adijsapjdsiao pdsi odji oapfji disoa pdsjiao fpdsjiao fdsajio fdsaj ifdosap jidos jdios jiso pfdjsiaofp djsaio fdpsjaiof dpsa jfidospa fjdisop fjdsiop fdjsaio pfds jfsa",
        "date_posted" : "october 22, 2019"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/admin")
def admin():
    pass

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for { form.username.data }", "green accent-3")
        return redirect(url_for("login"))
    return render_template("register.html", title="register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "nr5p@hotmail.com" and form.password.data == "password":
            flash(f"login successful", "green accent-3")
            return redirect(url_for("home"))
        else:
            flash("login unsuccessful", "red accent-3")
    return render_template("login.html", title="login", form=form)