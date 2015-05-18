from flask import Flask
import os,sqlite3

#'sqlite:///'
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('OPENSHIFT_DATA_DIR') is None:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'app.db')
else:
     basedir = os.environ['OPENSHIFT_DATA_DIR']

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DATABASE_PATH'] = os.path.join(basedir,'app_database.db')


def init_db():
    con = sqlite3.connect(app.config['DATABASE_PATH'])
    con.row_factory = sqlite3.Row

    con.execute("create table if not exists user_pas(id_u integer primary key unique, username text not null unique, pas text not null)")
    con.execute("create table if not exists users(id_u integer primary key autoincrement, name text not null, lastname text not null, epost text unique not null, profilepic text, numb_of_paths integer, number_of_steps integer, length_went integer)")
    con.execute("create table if not exists friends(id_f integer primary key autoincrement, id_u integer not null, id_u_friend integer)")
    con.execute("create table if not exists posts(id_p integer primary key autoincrement, id_u integer not null, name text, description text, photo_path_list text, position_list text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists comments(id_c integer primary key autoincrement, id_p integer not null, id_u integer not null,comment text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.execute("create table if not exists likes(id_l integer primary key autoincrement,id_p integer not null, id_u integer not null)")
    con.execute("create table if not exists friendrequests(id_fr integer primary key autoincrement, id_u integer, id_u_friend_request integer)")
    con.execute("create table if not exists postphotos(id_pp integer primary key autoincrement, photo text, id_p integer)")
    con.commit()
