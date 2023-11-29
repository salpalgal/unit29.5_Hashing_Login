from flask import Flask, render_template, request, redirect, jsonify, session, flash
from models import User, Feedback, db, connect_db
from forms import CreateUserForm, LoginForm, FeedbackForm

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


@app.route("/user/<username>/delete", methods = ["POST"])
def delete_user(username):
    if "username" not in session:
        flash("you must log in")
        return redirect("/login")
    else:
        user = User.query.filter(User.username == username). first()
        db.session.delete(user)
        db.session.commit()
        return redirect("/")


@app.route("/user/<username>/feedback/add", methods = ["GET","POST"])
def add_feedback(username):
    form = FeedbackForm()
    user = User.query.filter(User.username== username).first()
    if "username" not in session:
        flash("you must log in")
        return redirect("/login")
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feed = Feedback(title= title, content= content, username = username)
        db.session.add(feed)
        db.session.commit()
        return redirect(f"/user/{username}")
    else:
        return render_template("feedback.html", form= form, user= user)


@app.route("/feedback/<int:feedback_id>/update", methods = ["GET", "POST"])
def edit_feedback(feedback_id):
    form = FeedbackForm()
    feed = Feedback.query.get_or_404(feedback_id)
    if "username" not in session:
        flash("you must log in")
        return redirect("/login")
    if form.validate_on_submit():
        username = feed.user.username
        feed.title = form.title.data
        feed.content= form.content.data
        db.session.add(feed)
        db.session.commit()
        return redirect(f"/user/{username}")
    else:
        return render_template("edit.html", form = form, feed = feed)

@app.route("/feedback/<int:feedback_id>/delete", methods = ["POST"])
def delete_feedback(feedback_id):
    if "username" not in session:
        flash("you must log in")
        return redirect("/login")
    else:
        feed = Feedback.query.get_or_404(feedback_id)
        username= feed.user.username
        db.session.delete(feed)
        db.session.commit()
        return redirect(f"/user/{username}")

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


