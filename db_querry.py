from flask import Flask,json,request,g,Blueprint
import os,sqlite3
from config import app


def connect_db():
    connection = sqlite3.connect(app.config['DATABASE_PATH'])
    connection.row_factory = sqlite3.Row
    return connection

def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error):
    "Closses the database at the end of the request."
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def login(username, pasword):
    db = get_db()
    usernameQuery = db.execute("select * from user_pas where username=?",(username,))
    result = usernameQuery.fetchall()
    if (len(result) <= 0):
        return json.dumps({"result":"usernameError"})
    if (pasword == result[0]['pas']):
        return json.dumps({"result":result[0]['id_u']})
    return json.dumps({"result":"passwordError"})

def get_name(id_u):
    db = get_db()
    query = db.execute("SELECT NAME,LASTNAME FROM users where id_u=?",(id_u,))
    result = query.fetchall()
    if (len(result) >0):
        return json.dumps({"result":"ok","name":result[0]['name'],"lastname":result[0]['lastname']})
    else:
        return json.dumps({"result":"no user with that id_u"})

def get_post_from_user(id_u):
    db = get_db()
    query = db.execute("select * from posts where id_u=? ORDER BY timestamp DESC",(id_u,))
    result = query.fetchall()
    res = []
    for post in result:
        #get pictures
        likes = json.loads(get_post_likes(post['id_p']))
        comments = json.loads(get_comments(post['id_p']))
        name = json.loads(get_name(post['id_u']))
        res.append(json.dumps({"post_name":name['name'],"post_lastname":name['lastname'],"id_p":post['id_p'],
                              "name":post['name'],"description":post['description'],
                              "position_list":post['position_list'],"comments":comments['result'],"likes": likes["result"],
                              "photos":"[]"}))
    return json.jsonify({"result": res})

def get_friend_posts(id_u):
    db = get_db()
    query = db.execute("select id_u_friend from friends where id_u=?",(id_u,))
    friends = query.fetchall()
    res = []
    for friend in friends:
        res.append(friend['id_u_friend'])
    if (len(res) == 0):
        return json.jsonify({"result":"no Friends"})
    else:
        db_querry = 'SELECT * FROM posts where id_u in (%s) ORDER BY timestamp DESC'%','.join('?' for a in res)
        querry = db.execute(db_querry,res)
        result = querry.fetchall()
        res = []
        for post in result:
            #get pictures
            likes = json.loads(get_post_likes(post['id_p']))
            comments = json.loads(get_comments(post['id_p']))
            name = json.loads(get_name(post['id_u']))
            res.append(json.dumps({"post_name":name['name'],"post_lastname":name['lastname'],"id_p":post['id_p'],
                                   "name":post['name'],"description":post['description'],
                                   "position_list":post['position_list'],"comments":comments['result'],
                                   "likes": likes["result"],"photos":"[]"}))
        return json.jsonify({"result": res})

def post(id_u,name,description,position_list):
    db = get_db()
    db.execute("insert into posts (id_u,name,description,photo_path_list,position_list) values(?,?,?,?,?)",[id_u,name,description,"photo",position_list])
    db.commit()
    return json.jsonify({"result":"post added"})

def get_comments(id_p):
    db = get_db()
    query = db.execute("select * from comments where id_p=? order by timestamp DESC",(id_p,))
    result = query.fetchall()
    res = []
    for comment in result:
        name = json.loads(get_name(comment['id_u']))
        res.append([name['name']+name['lastname'],comment['comment']])
    return  json.dumps({"result": res})

def comment_post(id_p, id_u,comment):
    db = get_db()
    db.execute("insert into comments (id_p,id_u,comment) values(?,?,?)",[id_p,id_u,comment])
    db.commit()
    return json.jsonify({"result":"comment was added to post"})

def add_friend(id_u,id_u_friend):
    db = get_db()
    db.execute("insert into friends (id_u,id_u_friend) values(?,?)", (id_u, id_u_friend))
    db.commit()
    return json.jsonify({"result":"friend was added"})

def remove_friend(id_u, id_u_friend):
        db = get_db()
        db.execute("delete from friends where id_u=? and id_u_friend=?",(id_u,id_u_friend))
        db.commit()
        return json.jsonify({"result":"friend was removed"})

def get_friends(id_u):
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
    db = get_db()
    query = db.execute("select * from users where id_u=?",(id_u,))
    qresult = query.fetchall()
    if (len(qresult)>0):
        user = qresult[0]
        #get pic
        return json.jsonify({"name":user['name'],"lastname":user['lastname'],"email":user['epost'],
                             "numb_of_path":user['numb_of_paths'],"number_of_steps":user['number_of_steps'],
                             "length_went":user['length_went'],"photo_path_list":"[]"})
    else:
        return json.jsonify({'result':'exist no such user'})


def add_user(name,lastname,epost,username,pasword):
    db = get_db()
    try:
        db.execute("insert into users (name,lastname,epost,profilepic,numb_of_paths,number_of_steps,length_went) values(?,?,?,?,?,?,?)", [name,lastname,epost,"basic pic",0,0,0])
    except sqlite3.IntegrityError:
        return json.jsonify({"result":"emailError"})
    query = db.execute("select id_u from users where epost=?",(epost,))
    result = query.fetchall()[0]
    try:
        db.execute("insert into user_pas (id_u,username,pas) values(?,?,?)",[result['id_u'],username,pasword])
    except sqlite3.IntegrityError:
        return json.jsonify({"result":"usernameExistsError"})
    db.commit()
    return json.jsonify({"result":"user added"})

def get_post_likes(id_p):
    db = get_db()
    query = db.execute("select * from likes where id_p=?", (id_p,))
    qresult = query.fetchall()
    number_of_likes = 0
    for like in qresult:
        number_of_likes += 1
    return json.dumps({"result":number_of_likes})


def add_remove_post_like(id_p, id_u):
    db = get_db()
    querry = db.execute("select * from likes where id_p=? and id_u=?",(id_p,id_u))
    result = querry.fetchall()
    if (len(result) == 0):
        value_integrity = db.execute("select * from posts where id_p=?",(id_p,))
        value_result = value_integrity.fetchall()
        if (len(value_result) > 0):
            db.execute("insert into likes (id_p,id_u) values(?,?)",(id_p,id_u))
            db.commit()
            return json.jsonify({"result":"post was liked"})
        else:
            return json.jsonify({"result":"invalidInput"})
    else:
        db.execute("delete from likes where id_p=? and id_u=?",(id_p, id_u))
        db.commit()
        return json.jsonify({"result":"post like was removed"})

def user_search(id_u, partusername):
    db = get_db()
    querry = db.execute('select id_u,name,lastname from users where not id_u=? and name like ? or not id_u=? and lastname like ?',(id_u, "%"+partusername+"%", id_u, "%"+partusername+"%"))
    qresult = querry.fetchall()
    res = []
    for person in qresult:
        res.append([person['id_u'],person['name'],person['lastname']])
    return json.jsonify({"result":res})


def get_all_users():
    db = get_db()
    querry = db.execute("select * from users")
    qresult = querry.fetchall()
    result = []
    for user in qresult:
        result.append(json.dumps({"name":user['name'],"lastname":user['lastname'],"email":user['epost'],"id_u"user['id_u']}))
    return json.jsonify({"result":result})


def inittables():
    con = sqlite3.connect(app.config['DATABASE_PATH'])
    con.row_factory = sqlite3.Row

    con.execute("create table if not exists user_pas(id_u integer primary key unique, username text not null unique, pas text not null)")
    con.execute("create table if not exists users(id_u integer primary key autoincrement, name text not null, lastname text not null, epost text unique not null, profilepic text, numb_of_paths integer, number_of_steps integer, length_went integer)")
    con.execute("create table if not exists friends(id_f integer primary key autoincrement, id_u integer not null, id_u_friend integer)")
    con.execute("create table if not exists posts(id_p integer primary key autoincrement, id_u integer not null, name text, description text, photo_path_list text, position_list text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists comments(id_c integer primary key autoincrement, id_p integer not null, id_u integer not null,comment text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists likes(id_l integer primary key autoincrement,id_p integer not null, id_u integer not null)")
    con.commit()
    con.close()
    con.close()

inittables()
