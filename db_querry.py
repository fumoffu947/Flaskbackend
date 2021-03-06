from flask import Flask,json,request,g,Blueprint
import os,sqlite3
from config import app


def connect_db():
    ### conect to the database with the path from the app config ###
    connection = sqlite3.connect(app.config['DATABASE_PATH'])
    connection.row_factory = sqlite3.Row
    return connection

def get_db():
    ### connect to the database if it is not already connected ###
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error):
    "Closses the database at the end of the request."
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def login(username, pasword):
    ### fetches the id_u of the user ###
    ### returns the error id username or password is wrong ###
    db = get_db()
    usernameQuery = db.execute("select * from user_pas where username=?",(username,))
    result = usernameQuery.fetchall()
    if (len(result) <= 0):
        return json.dumps({"result":"usernameError"})
    if (pasword == result[0]['pas']):
        return json.dumps({"result":result[0]['id_u']})
    return json.dumps({"result":"passwordError"})

def get_name(id_u):
    ### fetches the name and lastname of the user of id id_u ###
    db = get_db()
    query = db.execute("SELECT NAME,LASTNAME FROM users where id_u=?",(id_u,))
    result = query.fetchall()
    if (len(result) >0):
        return json.dumps({"result":"ok","name":result[0]['name'],"lastname":result[0]['lastname']})
    else:
        return json.dumps({"result":"no user with that id_u"})

def get_post_from_user(id_u):
    ### fetches the posts uf the user ###
    db = get_db()
    query = db.execute("select * from posts where id_u=? ORDER BY timestamp DESC",(id_u,))
    result = query.fetchall()
    res = []
    for post in result:
        ### fetches the photos for the post ###
        photos = []
        photoquerry = db.execute("select photo from postphotos where id_p=?",(post['id_p'],))
        photoresult = photoquerry.fetchall()
        ### put the photos in a list to send ##
        for photo in photoresult:
            photos.append(photo['photo'])

        ### fethces number of likes, comments, and name, lasnt mane of post owner ###
        likes = json.loads(get_post_likes(post['id_p']))
        comments = json.loads(get_comments(post['id_p']))
        name = json.loads(get_name(post['id_u']))
        res.append(json.dumps({"post_name":name['name'],"post_lastname":name['lastname'],"id_p":post['id_p'],
                              "name":post['name'],"description":post['description'],
                              "position_list":post['position_list'],"comments":comments['result'],"likes": likes["result"],
                              "photos":photos}))
    return json.jsonify({"result": res})

def get_friend_follow_posts(id_u):
    ### fetches friends and the ones the users id follows and fetches the posts for them in descending order ###
    db = get_db()

    ###fetches friends###
    query = db.execute("select id_u_friend from friends where id_u=?",(id_u,))
    friends = query.fetchall()
    res = []
    for friend in friends:
        res.append(friend['id_u_friend'])

    ###fetches followa###
    querry = db.execute("select id_u_follow from follow where id_u=?", (id_u,))
    follows = querry.fetchall()
    for follow in follows:
        res.append(follow['id_u_follow'])

    ### if no friends or follows exist return the result##
    if (len(res) == 0):
        return json.jsonify({"result":"no Friends"})

    ### goes trough the users id_u in res and fetch the posts for them
    else:
        db_querry = 'SELECT * FROM posts where id_u in (%s) ORDER BY timestamp DESC'%','.join('?' for a in res)
        querry = db.execute(db_querry,res)
        result = querry.fetchall()
        res = []
        for post in result:
            ### fetches the pictures for the post ###
            photos = []
            photoquerry = db.execute("select photo from postphotos where id_p=?",(post['id_p'],))
            photoresult = photoquerry.fetchall()
            for photo in photoresult:
                photos.append(photo['photo'])

            ### fetches the number of likes,coments and the name and lastname of the post owner ###
            likes = json.loads(get_post_likes(post['id_p']))
            comments = json.loads(get_comments(post['id_p']))
            name = json.loads(get_name(post['id_u']))
            res.append(json.dumps({"post_name":name['name'],"post_lastname":name['lastname'],"id_p":post['id_p'],
                                   "name":post['name'],"description":post['description'],
                                   "position_list":post['position_list'],"comments":comments['result'],
                                   "likes": likes["result"],"photos":photos}))
        return json.jsonify({"result": res})

### split the Base64 picture string from JsonPost into separate strings and return a list ###
def getPhotoListFromString(photos):
    if (len(photos) > 0):
        photoList = photos.split(",")
    else:
        photoList = []
    return photoList


def post(id_u,name,description,position_list,photos,path_lenght):
    try:
        db = get_db()
        ### post the psth info in posts ###
        db.execute("insert into posts (id_u,name,description,photo_path_list,position_list) values(?,?,?,?,?)",[id_u,name,description,"photo",position_list])
        photoList = getPhotoListFromString(photos)
        ### fetches the id_p of the newly added path ###
        querry = db.execute("select id_p from posts where id_u=? and name=? and description=? and photo_path_list=? and position_list=?",[id_u,name,description,"photo",position_list])
        result = querry.fetchall()
        ### adds the photos for the path in pathphotos with id_p as the path id_p ###
        for photo in photoList:
            db.execute("insert into postphotos (photo, id_p) values (?,?)",(photo, result[0]['id_p']))

        ### updates the user ###
        path_querry = db.execute("select * from users where id_u=?", (id_u,))
        user_info = path_querry.fetchall()[0]
        db.execute("update users set numb_of_paths=? where id_u=?",(user_info['numb_of_paths']+1, id_u))
        db.execute("update users set length_went=? where id_u=?",(user_info['length_went']+path_lenght, id_u))
        db.commit()
        return json.jsonify({"result":"post added"})
    except:
        return json.jsonify({"result":"failed to post"})

def get_comments(id_p):
    ### fetches the comments of a path post and returns a list with comments (name lastname , comment) in descending order ####
    db = get_db()
    query = db.execute("select * from comments where id_p=? order by timestamp DESC",(id_p,))
    result = query.fetchall()
    res = []
    for comment in result:
        ### fetches the name of the comment owner ###
        name = json.loads(get_name(comment['id_u']))
        res.append([name['name']+name['lastname'],comment['comment']])
    return  json.dumps({"result": res})

def comment_post(id_p, id_u,comment):
    ### add a comment for a post ###
    db = get_db()
    db.execute("insert into comments (id_p,id_u,comment) values(?,?,?)",[id_p,id_u,comment])
    db.commit()
    return json.jsonify({"result":"comment was added to post"})

def add_remove_friend(id_u,id_u_friend):
    ### shal only be called if an friend request exists or to remove a friend relationship ###
    ### adds and removes friends depending on if the exist before or not ###
    db = get_db()
    ### checks if the friend relationship exists ###
    querry = db.execute("select * from friends where id_u=? and id_u_friend=?",(id_u,id_u_friend))
    qresult = querry.fetchall()
    if (len(qresult) == 0):
        ### adds the friend relation ship for both parties ###
        db.execute("insert into friends (id_u,id_u_friend) values(?,?)", (id_u, id_u_friend))
        db.execute("insert into friends (id_u,id_u_friend) values(?,?)", (id_u_friend, id_u))
        ### remove the friend request for both (if they exists) ###
        db.execute("delete from friendrequests where id_u=? and id_u_fr=? or id_u=? and id_u_fr=?",(id_u,id_u_friend,id_u_friend,id_u))
        db.commit()
        return json.jsonify({"result":"friend was added"})
    else:
        ### removes the friendrelationship for both users and messages ###
        db.execute("delete from friends where id_u=? and id_u_friend=?",(id_u,id_u_friend))
        db.execute("delete from friends where id_u=? and id_u_friend=?",(id_u_friend, id_u))
        db.execute("delete from messages where id_u=? and id_u_to=? or id_u=? and id_u_to=?", (id_u, id_u_friend, id_u_friend, id_u))
        db.commit()
        return json.jsonify({"result":"friend was removed"})

def add_remove_follow(id_u,id_u_follow):
    ### adds or removes the follow depending on if the users follows the other user or not ###
    db = get_db()
    querry = db.execute("select * from follow where id_u=? and id_u_follow=?",(id_u,id_u_follow))
    qresult = querry.fetchall()
    if (len(qresult) == 0):
        db.execute("insert into follow (id_u,id_u_follow) values(?,?)", (id_u, id_u_follow))
        db.commit()
        return json.jsonify({"result":"follow was added"})
    else:
        db.execute("delete from follow where id_u=? and id_u_follow=?",(id_u,id_u_follow))
        db.commit()
        return json.jsonify({"result":"follow was removed"})

def add_friend_request(id_u, id_u_friendrequest, removeRequest):
    ### adds or removes an friend request depending on removerequest ###
    db = get_db()
    querry = db.execute("select * from friendrequests where id_u=? and id_u_fr=?",(id_u,id_u_friendrequest))
    qresult = querry.fetchall()
    if (len(qresult) == 0):
        ### add request if it dont exist ###
        db.execute("insert into friendrequests (id_u,id_u_fr) values (?,?)",(id_u,id_u_friendrequest))
        db.commit()
        return json.jsonify({"result":"friend request added"})
    elif (removeRequest):
        ### remove the request ###
        db.execute("delete from friendrequests where id_u=? and id_u_fr=?",(id_u, id_u_friendrequest))
        db.commit()
        return json.jsonify({"result":"friend request was removed"})
    else:
        return json.jsonify({"result":"friend request already exists"})


def get_friend_requests(id_u):
    ###
    """
    gets the friends of user with id_u
    :param id_u:
    :return: a list of [id_u,name.lastname]
    """
    db = get_db()
    querry = db.execute("select * from friendrequests where id_u_fr=?", (id_u,))
    qresult = querry.fetchall()
    res = []
    for request in qresult:
        ### gets the name of the requester ###
        name = json.loads(get_name(request['id_u']))
        if (name['result'] == "ok"):
            res.append([request['id_u'],name['name'],name['lastname']])
    return json.jsonify({"result":res})

def add_message(id_u, id_u_to, message):
    ### adds a message from id_u to id_u_to ###
    db = get_db()
    db.execute("insert into messages (id_u,id_u_to,message) values (?,?,?)",(id_u,id_u_to,message))
    db.commit()
    return  json.jsonify({"result":"message added"})

def get_message(id_u, id_u_to):
    ### gets all messages from and to id_u and id_u_to and order them by descending order ###
    ### returns a list of [name+lastname, message, id_u] ###
    db = get_db()
    querry = db.execute("select * from messages where id_u=? and id_u_to=? or id_u=? and id_u_to=? ORDER BY timestamp ASC",(id_u,id_u_to,id_u_to,id_u))
    qresult = querry.fetchall()
    res = []
    for message in qresult:
        name = json.loads(get_name(message['id_u']))
        res.append([name['name']+name['lastname'],message['message'],message['id_u']])
    return json.jsonify({"result":res})

def get_friends(id_u):
    ### gets the frinds for the current user and returns them in a list ass [id_u_friend, name, lastname] ###
    db = get_db()
    query = db.execute("select id_u_friend from friends where id_u=?", (id_u,))
    qresult = query.fetchall()
    res = []
    for friend in qresult:
        name = json.loads(get_name(friend['id_u_friend']))
        if (name['result'] == "ok"):
            res.append([friend['id_u_friend'],name['name'],name['lastname']])
    return json.jsonify({"result":res})

def get_user(id_u):
    ### gets the user of given id_u ###
    db = get_db()
    query = db.execute("select * from users where id_u=?",(id_u,))
    qresult = query.fetchall()
    if (len(qresult)>0):
        user = qresult[0]
        stringPic = get_user_Pic(id_u)
        return json.jsonify({"name":user['name'],"lastname":user['lastname'],"email":user['epost'],
                             "numb_of_path":user['numb_of_paths'],
                             "length_went":user['length_went'],"profilepic":stringPic})
    else:
        return json.jsonify({'result':'exist no such user'})


def add_user(name,lastname,epost,username,pasword):
    ### adds a user and password ###
    ### if no constrains is detected then returns user added ###
    db = get_db()
    try: ### trys to add user. If unique constrain is detected then an emailError is sent back ###
        db.execute("insert into users (name,lastname,epost,numb_of_paths,length_went) values(?,?,?,?,?)", [name,lastname,epost,0,0])
    except sqlite3.IntegrityError:
        return json.jsonify({"result":"emailError"})
    query = db.execute("select id_u from users where epost=?",(epost,))
    result = query.fetchall()[0]
    try: ### if unique constrain is detected on username then returns usernameError ###
        db.execute("insert into user_pas (id_u,username,pas) values(?,?,?)",[result['id_u'],username,pasword])
    except sqlite3.IntegrityError:
        return json.jsonify({"result":"usernameExistsError"})
    db.commit()
    return json.jsonify({"result":"user added"})

def update_user_pic(id_u, pictureString):
    ### updates the user picture###
    ### id no picture exist for the current user then it is added ###
    db = get_db()
    querry = db.execute("select * from userpic where id_u=?",(id_u,))
    qresult = querry.fetchall()
    if (len(qresult) == 0):
        db.execute("insert into userpic (id_u, photo) values(?,?)", (id_u, pictureString))
        db.commit()
        return json.jsonify({"result":"updated profilepic"})
    else:
        try:
            db.execute("UPDATE userpic SET photo = ? where id_u=?", (pictureString, id_u))
            db.commit()
            return json.jsonify({"result":"updated profilepic"})
        except:
            return json.jsonify({"result":"failed to add profilepic"})

def get_user_Pic(id_u):
    ### returns the user picture ###
    db = get_db()
    querry = db.execute("select * from userpic where id_u=?", (id_u,))
    qresult = querry.fetchall()
    if (len(qresult) == 0):
        return ""
    else:
        return qresult[0]['photo']

def get_post_likes(id_p):
    ### gets the number of likes of a given post ###
    ### returns the number of likes in an JsonObject ###
    db = get_db()
    query = db.execute("select * from likes where id_p=?", (id_p,))
    qresult = query.fetchall()
    number_of_likes = 0
    for like in qresult:
        number_of_likes += 1
    return json.dumps({"result":number_of_likes})


def add_remove_post_like(id_p, id_u):
    ### add or removes a like from a post depending on if it exists before or not ###
    db = get_db()
    querry = db.execute("select * from likes where id_p=? and id_u=?",(id_p,id_u))
    result = querry.fetchall()
    if (len(result) == 0):
        ### ses if there exists a post of that id and adds the like else returns error ###
        value_integrity = db.execute("select * from posts where id_p=?",(id_p,))
        value_result = value_integrity.fetchall()
        if (len(value_result) > 0):
            db.execute("insert into likes (id_p,id_u) values(?,?)",(id_p,id_u))
            db.commit()
            return json.jsonify({"result":"post was liked"})
        else:
            return json.jsonify({"result":"invalidInput"})
    else:
        ### removes the like if postlike already exists ###
        db.execute("delete from likes where id_p=? and id_u=?",(id_p, id_u))
        db.commit()
        return json.jsonify({"result":"post like was removed"})

def user_search(id_u, partusername):
    ### searches for user with given partusername ###
    ### return a list of all found users ###
    db = get_db()
    querry = db.execute('select id_u,name,lastname from users where not id_u=? and name like ? or not id_u=? and lastname like ?',(id_u, "%"+partusername+"%", id_u, "%"+partusername+"%"))
    qresult = querry.fetchall()
    res = []
    for person in qresult:
        res.append([person['id_u'],person['name'],person['lastname']])
    return json.jsonify({"result":res})


def inittables():
    con = sqlite3.connect(app.config['DATABASE_PATH'])
    con.row_factory = sqlite3.Row

    con.execute("create table if not exists user_pas(id_u integer primary key unique, username text not null unique, pas text not null)")
    con.execute("create table if not exists users(id_u integer primary key autoincrement, name text not null, lastname text not null, epost text unique not null, numb_of_paths integer, length_went integer)")
    con.execute("create table if not exists friends(id_f integer primary key autoincrement, id_u integer not null, id_u_friend integer)")
    con.execute("create table if not exists posts(id_p integer primary key autoincrement, id_u integer not null, name text, description text, photo_path_list text, position_list text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists comments(id_c integer primary key autoincrement, id_p integer not null, id_u integer not null,comment text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists likes(id_l integer primary key autoincrement,id_p integer not null, id_u integer not null)")
    con.execute("create table if not exists postphotos(id_pp integer primary key autoincrement, photo text, id_p integer)")
    con.execute("create table if not exists follow(id_f integer primary key autoincrement, id_u integer, id_u_follow integer)")
    con.execute("create table if not exists friendrequests(id_r integer primary key autoincrement, id_u integer, id_u_fr integer)")
    con.execute("create table if not exists messages(id_m integer primary key autoincrement, id_u integer, id_u_to integer, message text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists userpic(id_up integer primary key autoincrement, id_u unique not null, photo text)")
    con.commit()
    con.close()

#inittables()
