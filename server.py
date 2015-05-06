from flask import Flask,request,json
from config import basedir,app
from db_querry import *


@app.route("/")
def hello():
    get_db()
    return "Hello World!"

@app.route("/getuserpost" ,methods=["GET","POST"])
def get_user_posts():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return get_post_from_user(res['result'])

@app.route("/getuserflowpost" ,methods=["GET","POST"])
def getFlowPosts():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return get_friend_posts(res['result'])

@app.route("/adduser" ,methods=["GET","POST"])
def adduser():
    postInfo = request.get_json(force=True)
    return add_user(postInfo['name'],postInfo['lastname'],postInfo['epost'],postInfo['username'],postInfo['pasword'])

@app.route("/getuser", methods=["GET","POST"])
def getuser():
    postinfo = request.get_json(force=True)
    return get_user(postinfo['id_u'])

@app.route("/login",methods=["GET","POST"])
def userLogin():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return json.jsonify({"result":res['result']})

@app.route("/postpath", methods=["GET","POST"])
def postPath():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return post(res['result'],postinfo['name'],postinfo['description'],postinfo['position_list'])

@app.route("/postcomment",methods=['GET','POST'])
def postcomment():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return  comment_post(postinfo['id_p'],res['result'],postinfo['comment'])

@app.route("/getfriends",methods=['GET','POST'])
def getFriends():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return get_friends(res['result'])

@app.route("/addfriend", methods=['GET','POST'])
def addfriend():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['pasword']))
    return add_friend(res['result'], postinfo['id_u_friend'])

@app.teardown_appcontext
def close(error):
    close_db(error)





if __name__ == "__main__":
    app.run()
