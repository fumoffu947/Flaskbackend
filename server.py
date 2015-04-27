from flask import Flask,request,json
from rest_api_app import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
def hello():
    get_db()
    return "Hello World!"

#@app.route("/userpost")
#@app.route("/userfriendpost")
#def getfriendsposts():

@app.route("/adduser")
def adduser():
    postInfo = request.get_json(force=True)
    return add_user(postInfo['name'],postInfo['lastname'],postInfo['epost'],postInfo['username'],postInfo['pasword'])
    

@app.route("/user", methods=["GET","POST"])
def getuser():
    #httpinfo = request.get_json(force=True)
    #return get_user(httpinfo['id_u'])
    return get_user(1)

@app.route("/login",methods=["POST"])
def userLogin():
    httpinfo = request.get_json(force=True)
    return login(username,pasword)





if __name__ == "__main__":
    app.run()
