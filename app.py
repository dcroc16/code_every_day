from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "{name: David}"

@app.route("/login")
def login():
    return "<h1>Log In Page<h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


