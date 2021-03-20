from flask import Flask,render_template,request
from flask_pymongo import PyMongo
import os
app = Flask(__name__)
app.config["MONGO_URI"]=os.getenv("MONGO_URI")
@app.route("/")
def main():
    return render_template("home.html")
@app.route("/login")
def login():
    return "Welcome to login"

@app.route("/signup", methods = ["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")



if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0",debug=True)