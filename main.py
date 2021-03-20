from flask import Flask,render_template,request,redirect,url_for,session
from flask_pymongo import PyMongo
import bcrypt
import os
from utilities import encryption
import random
app = Flask(__name__)
app.config["MONGO_URI"]=os.getenv("MONGO")
app.secret_key = "NICe"
client = PyMongo(app)
db = client.db["hospitaldata"]
@app.route("/")
def main():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "form submitted"
    else:
        return render_template("login.html")

@app.route("/signup",methods = ["POST","GET"])
def signup():
    if "email" in session:
        return redirect(url_for("dashboard"))
    if request.method == "GET":
            return render_template("signup.html")
    elif request.method == "POST":
        commitdata = {}
        form = {}
        formdata = request.form
        for key in formdata:
            form[key] = formdata[key]
        if form["password"] != form["password2"]:
            return render_template("signup.html")
        check = db.find_one({"email":form["email"]})
        print(check)
        if check != None:
            return render_template("signup.html")
        _id = random.randint(10000000,999999999)
        salt = os.urandom(16)
        password = form["password"]
        commitdata["_id"] = _id
        session["email"] = form["email"]
        hashedpw = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        commitdata["password"] = hashedpw
        commitdata["email"] = form["email"]
        commitdata["salt"] = salt
        key = encryption.getKey(form["password"],salt)
        session["key"] = key
        db.insert_one(commitdata)
        hospdb = client.db[form["email"]]
        hospdb.insert_one({"random":0})
        hospdb.delete_one({"random":0})
        return redirect(url_for("dashboard"))

@app.route("/dashboard",methods = ["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")
@app.route("/logout")
def logout():
    if "email" in session and "key" in session:
        session.pop("email")
        session.pop("key")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0",debug=True)
