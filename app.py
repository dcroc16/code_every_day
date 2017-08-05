from flask import Flask, render_template, redirect, url_for, request, session, g
import config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


app = Flask(__name__)
app.config["SECRET_KEY"] = config.APP_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.DEV_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String)

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email

    def set_password(self, password):
        self.password =  generate_password_hash(password)

    def check_password(self, password):
        return  check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class UserForm(Form):
    username = StringField("username", validators=[Required()])
    password = PasswordField("password", validators=[Required()])
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500




@app.before_request
def before_request():
    for i in session:
        print(i)


@app.route("/")
def index():
    if current_user:
        user = current_user
    else:
        user = User(username="")
    return render_template("index.html", user=user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are now logged out"


@app.route("/login", methods=["POST", "GET"])
def login():
    form = UserForm()
    message = ""
    if request.method == "POST":
        the_user = User.query.filter_by(username=request.form["username"]).first()
        message = ""
        if the_user:
            if the_user.check_password(request.form["password"]):
                login_user(the_user)
                return redirect(url_for("index"))
            else:
                message = "Invalid Credentials"
        else:
            message = "Invalid Credentials"

    if current_user:
        user = current_user
    else:
        user = User(username="", password="", email="")   
    return render_template("login.html", message=message, form=form, user=user)


@app.route("/protected")
@login_required
def protected():
    return "the current user is: " + current_user.username


@app.route("/alarm_clock")
@login_required
def alarm():
    return render_template("alarm_clock.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


