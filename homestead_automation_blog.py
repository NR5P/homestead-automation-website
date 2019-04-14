from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "0d1ca5c04c3bcb857ed2488007e88640"

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
        flash(f"Account created for { form.username.data }", "green accent-3")
        return redirect(url_for("home"))
    return render_template("register.html", title="register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="login", form=form)

if __name__ == "__main__":
    app.run(debug=True)
