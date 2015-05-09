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
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return get_post_from_user(res['result'])

@app.route("/getuserflowpost" ,methods=["GET","POST"])
def getFlowPosts():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return get_friend_posts(res['result'])

@app.route("/adduser" ,methods=["GET","POST"])
def adduser():
    postInfo = request.get_json(force=True)
    return add_user(postInfo['name'],postInfo['lastname'],postInfo['email'],postInfo['username'],postInfo['password'])

@app.route("/getuser", methods=["GET","POST"])
def getuser():
    postinfo = request.get_json(force=True)
    return get_user(postinfo['id_u'])

@app.route("/login",methods=["GET","POST"])
def userLogin():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    print(res)
    return json.jsonify({"result":res['result']})

@app.route("/postpath", methods=["GET","POST"])
def postPath():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return post(res['result'],postinfo['name'],postinfo['description'],postinfo['position_list'])

@app.route("/postcomment",methods=['GET','POST'])
def postcomment():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return  comment_post(postinfo['id_p'],res['result'],postinfo['comment'])

@app.route("/getfriends",methods=['GET','POST'])
def getFriends():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return get_friends(res['result'])

@app.route("/addfriend", methods=['GET','POST'])
def addfriend():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return add_friend(res['result'], postinfo['id_u_friend'])

@app.route("/delete/removefriend", methods=['GET','POST'])
def removefriends():
    postinfo = request.get_json(force=True)
    res = json.loads(login(postinfo['username'],postinfo['password']))
    return remove_friend(res['result'],postinfo['id_u_friend'])

@app.route("/addremovelike", methods=['GET','POST'])
def addremovelike():
    postinfo = request.get_json(force=True)
    login_id = json.loads(login(postinfo['username'],postinfo['password']))
    return add_remove_post_like(postinfo['id_p'], login_id['result'])

@app.route("/test/gettall", methods=['GET'])
def getallusers():
    return get_all_users()

@app.teardown_appcontext
def close(error):
    close_db(error)





if __name__ == "__main__":
    app.run()
