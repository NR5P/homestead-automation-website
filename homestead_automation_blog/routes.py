from flask import render_template, url_for, redirect, flash, request
from homestead_automation_blog import app, db, bcrypt
from homestead_automation_blog.forms import RegistrationForm, LoginForm
from homestead_automation_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("login unsuccessful, check email and password", "red accent-3")
    return render_template("login.html", title="login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="account")




















