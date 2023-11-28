from flask import Flask, render_template, request, redirect, jsonify, session, flash
from models import User, db, connect_db
from forms import CreateUserForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/register" , methods = ["GET", "POST"])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User(username = username, password = password, email = email, first_name = first_name, last_name= last_name)
        db.session.add(user)
        db.session.commit()
        return redirect("/secret")
    else:
        return render_template("register.html", form =form)

@app.route("/")
def home():
    return redirect("/register")

@app.route("/login" ,methods= ["GET" ,"POST"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username).first()
        if user.password == password:
            session["username"] = username
            return redirect(f"/user/{username}")
        else: 
            flash("Invalid username/password")
    return render_template("login.html" , form= form)

@app.route("/user/<username>")
def userPage(username):
    user = User.query.filter(User.username == username).first()
    if "username" not in session:
        flash("you must log in")
        return redirect("/login")
    else:
        return render_template("user.html", user= user)

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

