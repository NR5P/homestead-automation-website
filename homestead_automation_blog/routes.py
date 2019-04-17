import secrets
import os
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from homestead_automation_blog import app, db, bcrypt
from homestead_automation_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    # resize picture to keep from saving to large of picture to data base
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated", "green accent-3")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="account", image_file=image_file, form=form)




















