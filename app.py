from flask import Flask,render_template,request,redirect,url_for,session
from flask_pymongo import PyMongo
import bcrypt
import os
from utilities import encryption
import random
from functools import wraps
app = Flask(__name__)
app.config["MONGO_URI"]=os.getenv("MONGO")
app.secret_key = "NICe"
client = PyMongo(app)
db = client.db["hospitaldata"]
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session and "key" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
@app.route("/")
def main():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session and "key" in session:
        return redirect(url_for("dashboard"))
    else:
        if request.method == "POST":
            formdata = request.form 
            form = {}
            for key in formdata:
                form[key] = formdata[key]
            email = form["email"]
            user = db.find_one({"email":email})
            if user == None:
                return render_template("login.html")
            storedpw = user["password"]
            givenpw = form["password"]
            salt = user["salt"]
            if bcrypt.checkpw(givenpw.encode(),storedpw):
                session["key"] = encryption.getKey(givenpw,salt)
                session["email"] = email
                return redirect(url_for("dashboard"))
            return render_template("login.html")
        else:
            return render_template("login.html")

@app.route("/signup",methods = ["POST","GET"])
def signup():

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
@login_required
def dashboard():
    hospdb = client.db[session["email"]]
    

    if request.method == "GET":
        allpatients = list(hospdb.find({}))
        decryptedallpatients = []
        for document in allpatients:
            decdoc = {}
            for index in document:
                encrypted = document[index]
                if index != "_id":
                    decrypted = encryption.decrypt(session["key"],encrypted)
                    decdoc[index] = decrypted
                else:
                    decdoc[index] = encrypted
            decryptedallpatients.append(decdoc)
        return render_template("dashboard.html",patientdata = decryptedallpatients)
    elif request.method == "POST":
        formdata = request.form 
        patient = {}
        for key in formdata:
            currententry = formdata[key]
            encryptedentry = encryption.encrypt(session["key"],currententry)
            patient[key] = encryptedentry
        patient["_id"] = random.randint(1000000,999999999)
        hospdb.insert_one(patient)
        return redirect(url_for("dashboard"))
        
@app.route("/logout")
def logout():
    if "email" in session and "key" in session:
        session.pop("email")
        session.pop("key")
    return redirect(url_for("login"))
@app.route("/edit/<id>", methods = ["GET","POST"])
@login_required
def edit(id):
    hospdb = client.db[session["email"]]
    id = int(id)
    if request.method == "GET":
        alldata = {}
        currentpatient = hospdb.find_one({"_id":id})
        if currentpatient == None:
            return redirect(url_for("dashboard"))
        del currentpatient["_id"]
        for key in currentpatient:
            currentencrypted = currentpatient[key]
            decrypted = encryption.decrypt(session["key"],currentencrypted)
            alldata[key] = decrypted
        return render_template("edit.html",patientdata = alldata)
    elif request.method == "POST":
        formdata = request.form
        encrypteddata = {}
        for key in formdata:
            unencdata = formdata[key]
            encdata = encryption.encrypt(session["key"],unencdata)
            encrypteddata[key] = encdata
        hospdb.update_one({"_id":id},{"$set":encrypteddata})
        return redirect(url_for("dashboard"))




if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0",debug=True)
