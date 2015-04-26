from flask import Flask,json,request,g
import os,sqlite3


def connect_db():
    connection = sqlite3.connect('app_database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_db():
   # if not hasattr(g,'sqlite_db'):
   #     g.sqlite_db = connect_db()
   # return g.sqlite_db
    return connect_db()

def close_db(error):
    "Closses the database at the end of the request."
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def login(username, pasword):
    db = get_db()
    usernameQuery = db.execute("select * from user_pas where username=?",(username,))
    result = usernameQuery.fetchall()[0]
    if (len(result) <= 0):
        return "{result:usernameError}"
    if (pasword == result['pas']):
        return json.jsonify({"result":result['id_u']})
        #return json.dumps({"result":result['id_u']})        
    return "{result:paswordError}"

def get_name(id_u):
    db = get_db()
    query = db.execute("SELECT NAME,LASTNAME FROM users where id_u=?",(id_u,))
    result = query.fetchall()
    return json.jsonify({"name":result[0]['name'],"lastname":result[0]['lastname']})
    #return json.dumps({"name":result[0]['name'],"lastname":result[0]['lastname']})

def get_post_from_user(id_u):
    db = get_db()
    query = db.execute("select * from posts where id_u=? ORDER BY timestamp DESC",(id_u,))
    result = query.fetchall()
    res = []
    for post in result:
        #get pictures
        name = json.loads(get_name(post['id_u']))
        res.append([name['name'],name['lastname'],post['id_p'],post['name'],post['description'],post['position_list']])
    return json.jsonify({"result": res})
    #return json.dumps({"result": res})

#def get_friend_posts(id_u):
    #db = get_db()
    #query = db.execute("select id_u_friend from friends where id_u=?",(id_u,))
    #friends = query.fetchall()
    #res = []

def post(id_u,name,description,position_list):
    db = get_db()
    db.execute("insert into posts (id_u,name,description,photo_path_list,position_list) values(?,?,?,?,?)",[id_u,name,description,"photo",position_list])
    db.commit()

def get_coments(id_p):
    db = get_db()
    query = db.execute("select * from comments where id_p=? order by timestamp DESC",(id_p,))
    result = query.fetchall()
    res = []
    for comment in result:
        name = json.loads(get_name(comment['id_u']))
        res.append([name['name']+name['lastname'],comment['comment']])
    return  json.jsonify({"result": res})
    #return  json.dumps({"result": res})

def comment_post(id_p, id_u,comment):
    db = get_db()
    db.execute("insert into comments (id_p,id_u,comment) values(?,?,?)",[id_p,id_u,comment])
    db.commit()

def get_friends(id_u):
    db = get_db()
    query = db.execute("select id_u_friend from friends where id_u=?",(id_u,))
    qresult = query.fetchall()
    res = []
    for friend in qresult:
        res.append(friend['id_u_friend'])
    return json.jsonify({"result":res})
    #return json.dumps({"result":res})

def get_user(id_u):
    db = get_db()
    query = db.execute("select * from users where id_u=?",(id_u,))
    qresult = query.fetchall()
    user = qresult[0]
    #get pic
    return json.jsonify({"name":user['name'],"lastname":user['lastname'],"epost":user['epost'],"numb_of_path":user['numb_of_paths'],"number_of_steps":user['number_of_steps'],"length_went":user['length_went']})
    #return json.dumps({"name":user['name'],"lastname":user['lastname'],"epost":user['epost'],"numb_of_paths":user['numb_of_paths'],"number_of_steps":user['number_of_steps'],"length_went":user['length_went']})
