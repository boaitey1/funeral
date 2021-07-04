from flask import Flask, render_template, url_for,  request, redirect, flash
from db import DB
from sms import SMS
from methods import *

app = Flask(__name__)
app.secret_key = b'E_5N#yO2LC"FH4QS8zEffMhgf46@@]'

gideon = "0208162005" #0208162005
ekow = "0550726756" #0550726756
general_family = "0208162005" #0546353625
augusta = "0546353625"

TABLE_NAME = "contributor"



@app.route("/")
def index():
    return render_template("index.html")


 

@app.route("/donations", methods=["POST","GET"])
def donations():

    contributor_name = ""
    contributor_contact =""

    amount = ""  #accumulator

    if request.method == "POST":
        db = DB()
        name = request.form["name"]
        contact = str(request.form["contact"])
        amount = str(request.form["amount"])
        beneficiary = request.form["beneficiary"]

        contributor_name = name
        contributor_contact = contact

        db.insert(TABLE_NAME, "name", "contact", "amount", "beneficiary", name, contact, amount, beneficiary)
        
        if beneficiary == "Gideon":
            beneficiary_sms(contributor_name, amount, contributor_contact, beneficiary, gideon)
            
        elif beneficiary == "Ekow":
            beneficiary_sms(contributor_name, amount, contributor_contact, beneficiary, ekow)
        
        elif beneficiary == "General Family":
            beneficiary_sms(contributor_name, amount, contributor_contact, beneficiary, general_family)
        elif beneficiary == "Augusta":
            beneficiary_sms(contributor_name, amount, contributor_contact, beneficiary,augusta)
        
        flash("Successful")
        return redirect(url_for("donations"))

    return render_template("donations.html")




@app.route("/donations/admin", methods = ["GET", "POST"])
def admin():
    db = DB()
    contributors = db.select_all(TABLE_NAME)
    lenght = len(contributors)

    if request.method == "POST":
        db.delete_rows(TABLE_NAME)
        print("deleted")
    return render_template("admin.html", contributors = contributors, lenght = lenght)


@app.route("/thanks")
def thanks():
    return render_template("appreciation.html")




if __name__ == "__main__":
    app.run(debug = True)
    
