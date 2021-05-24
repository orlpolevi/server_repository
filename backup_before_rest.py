#set FLASK_APP=server.py
# flask run

from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://ormatan:Ormatanormatan123@cluster0.ayazu.mongodb.net/test?retryWrites=true&w=majority")
app.db = client.test

#---------------------------------------------------------------------#
                           #testing only#
#---------------------------------------------------------------------#
testing = ["bloop","poop"]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def test1():
    #testing.append(app.db.test.find({}))
    #app.db.test.insert({"dbtest":"test"}) #working
    return render_template("index.html")

@app.route("/test2")
def test2():
    return render_template("testpage.html")

@app.route("/db", methods =["GET", "POST"])
def db():
    temp = app.db.test.find_one({"name":"Michael"})
    return render_template("db.html", testing = testing,temp=temp)
#---------------------------------------------------------------------#
                            #server utilities#
#---------------------------------------------------------------------#

#working as intented with hard coded check, need to check response from client
@app.route("/login", methods =["POST"])
def login():
    login_info_from_client_name = request.form["name"]
    login_info_from_client_password = request.form["password"]
    user_info_from_db = app.db.test.find_one({"name":login_info_from_client_name})

    if user_info_from_db!=None:
        if user_info_from_db["password"] == login_info_from_client_password:
            logged_flag = {"$set":{"logged":True}}
            app.db.test.update_one(user_info_from_db, logged_flag )

#need to add return value if not ok


@app.route("/activate_GA", methods =["GET", "POST"])
def activate_GA():
    #call the run method from ga.py with parameters => name of student and preferences, returned value should be a dict with congruencd individuals
    #return json with individuals
    pass

@app.route("/add_user",  methods =["GET", "POST"])
def add_user():
    pass
    

if __name__ == '__main__':
    app.run()