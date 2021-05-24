#set FLASK_APP=server.py
# flask run

from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from ga import initialize

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb+srv://ormatan:Ormatanormatan123@cluster0.ayazu.mongodb.net/test?retryWrites=true&w=majority")
app.db = client.test

parser = reqparse.RequestParser()




#---------------------------------------------------------------------#
                           #testing only#
#---------------------------------------------------------------------#
testing = ["bloop","poop"]

#---------------------------------------------------------------------#
                           #rest api test#
#---------------------------------------------------------------------#
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}, 201
api.add_resource(HelloWorld, '/hello')

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

#working!
class testing_parser(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('age', type=str)
        args = parser.parse_args()

        return {
            'status': True,
            'name': '{} added. Good'.format(args['name']),
            'age': '{} added. Good'.format(args['age'])
        }
api.add_resource(testing_parser, '/testing parser')





#---------------------------------------------------------------------#
                        #server utility functions#
#---------------------------------------------------------------------#

def get_user_from_db(name):
    user_info = app.db.test.find_one({"name":name})
    return user_info



#---------------------------------------------------------------------#
                            #server utilities#
#---------------------------------------------------------------------#

#working as intented with hard coded check, need to check response from client
@app.route("/login", methods =["POST"])
def login():
    login_info_from_client_email = request.form["email"]
    login_info_from_client_password = request.form["password"]
    user_info_from_db = app.db.test.find_one({"name":login_info_from_client_email})

    if user_info_from_db!=None:
        if user_info_from_db["password"] == login_info_from_client_password:
            logged_flag = {"$set":{"logged":True}}
            app.db.test.update_one(user_info_from_db, logged_flag )

#need to add return value if not ok

class Activate_GA(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('course', type=str)
        args = parser.parse_args()
        return print(type(initialize(args["name"], args["course"])))
        pass

class get_user_info(Resource):
    def get(self, name):
        #this function will get a name from the client and return its info for the manager 
        user_info = get_user_from_db(name)
        return jsonify(user_info["name"],user_info["department"], user_info["coursesProvide"], user_info["daysProvide"] )
        
class add_user_to_db(Resource):
    def get(self, name, lastname, department):
        #this function will get kwargs from client form and add it to the database - manual adding for manager
        
        #user_dict = {"name": name, "lastname": lastname,"department": department}
        #app.db.test.insert_one(user_dict)
      
        try:
            if get_user_from_db(name)!=None:
                user_dict = {"name": name, "lastname": lastname,"department": department}
                app.db.test.insert_one(user_dict)  
        except:
            pass
            #raise error -> user is already in the database
        #finally:
            return jsonify(user_dict["name"],user_dict["lastname"],user_dict["department"])
        pass


#not tested yet - without using parser
class register_user2(Resource):
    def post(self, name, lastname, password, gender, email, phone):
        try:
            if get_user_from_db(name)!=None:
                user_dict = {"name": name, "lastname": lastname, "password": password, "gender":gender, "email":email, "phone":phone}
                app.db.test.insert_one(user_dict)
        except:
            pass

#not tested yet
class register_user(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('lastname', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('gender', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone', type=str)
        args = parser.parse_args()

        if get_user_from_db(args['name'])==None:
                app.db.test.insert_one(args)
                return {
                 'status': "ok",
                    'name': '{} '.format(args['name']),
                    'lastname': '{}'.format(args['lastname']),
                    'password': '{}'.format(args['password']),
                 'gender': '{}'.format(args['gender']),
                 'email': '{}'.format(args['email']),
                 'phone': '{}'.format(args['phone'])
                }
        else:
                return {'msg':"user is already in the database"}        
            
        



api.add_resource(Activate_GA, '/activate_GA')
api.add_resource(get_user_info, '/getuser/<string:name>')
api.add_resource(add_user_to_db, '/adduser/<string:name>/<string:lastname>/<department>')
api.add_resource(register_user, '/register')

if __name__ == '__main__':
    app.run(debug=True)