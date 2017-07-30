from flask import Flask, render_template, redirect, url_for, request
import config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = config.APP_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.DEV_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



class User(db.Model):
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    
    if request.method == "POST":
        message = "Logged In " + request.form["username"]
        current_user = User.query.filter_by(username=request.form["username"]).first()
        if current_user:
	    message += " : " + current_user.email
            if current_user.check_password(request.form["password"]):
                message += " : " + " valid password "
            else:
                message += " : "  + "invalid password"
        
    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


