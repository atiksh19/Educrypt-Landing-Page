from flask import Flask, render_template, url_for, request
from pymongo import MongoClient
from json import dumps
# Configure Database
conn_str = "mongodb+srv://Atiksh:BAKOzinbCcHzXLh0@cluster0.h8feh.mongodb.net/EducryptDatabase?ssl=true&ssl_cert_reqs=CERT_NONE"

def uploadJson(data):
    DBclient = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    myDB = DBclient["EducryptDatabase"]["preferences"]
    myDB.insert_one(data)

def errorhandlerSelf(data):
    errors = []
    if(data["name"] == ""):
        errors.append("Name cannot be empty")
    if(data["discord"] == ""):
        errors.append("Discord id cannot be empty")
    elif((data["discord"][-5:][0] != "#") or (data["discord"][-4:].isdigit() == False)):
        errors.append("Discord id is not valid")
    return errors

def errorhandlerGroup(data):
    errors = []
    if(data["name"] == ""):
        errors.append("Name cannot be empty")
    if(len(data["discord"]) < 1):
        errors.append("More than 1 Discord ids needed")
    for dc in data["discord"]:
        if(dc==""):
            continue
        if((data["discord"][-5:][0] != "#") or (data["discord"][-4:].isdigit())):
            errors.append("One or more of the Discord ids is/are invalid")
            break
    return errors

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("./index.html")

@app.route("/form")
def form():
    return render_template("./form.html", load="choice")

@app.route("/register_self", methods=['POST'])
def register_self():
    if request.method == 'POST':
        data = {
            "_id": request.form["discord"],
            "discord": request.form["discord"],
            "name": request.form["name"],
            "interval": request.form["interval"],
            "course": request.form["course"]
        }
        errs = errorhandlerSelf(data)
        if(errs == []):
            uploadJson(data)
            return render_template('./form.html', load="success")
        else:
            return render_template('./form.html', load="self", errors=errs)

@app.route("/register_group", methods=['POST'])
def register_group():
    if request.method == 'POST':
        data = {
            "_id": "",
            "discord": request.form["discord"].split(';'),
            "name": request.form["name"],
            "interval-course": request.form["interval-course"],
            "interval-meet": request.form["interval-meet"],
            "course": request.form["course"]
        }
        errs = errorhandlerGroup(data)
        if(errs == []):
            uploadJson(data)
            return render_template('./form.html', load="success")
        else:
            return render_template('./form.html', load="group", errors=errs)

if __name__ == "__main__":
    app.run()