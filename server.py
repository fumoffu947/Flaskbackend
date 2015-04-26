from flask import Flask,request,json
from rest_api_app import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

#@app.route("/userpost")
#@app.route("/userfriendpost")
#def getfriendsposts():
    

@app.route("/user", methods=["POST"])
def getuser():
    httpinfo = request.get_json(force=True)
    return get_user(httpinfo['id_u'])

@app.route("/login",methods=["POST"])
def userLogin():
    httpinfo = request.get_json(force=True)
    return login(username,pasword)





if __name__ == "__main__":
    app.run()
