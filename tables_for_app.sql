create table if not exists user_pas(id_u integer primary key unique, username text not null unique, pas text not null);
create table if not exists users(id_u integer primary key autoincrement, name text, lastname text, epost text unique, profilepic text, numb_of_paths integer, number_of_steps integer, length_went integer);
create table if not exists friends(id_f integer primary key autoincrement, id_u integer, id_u_friend integer);
create table if not exists posts(id_p integer primary key autoincrement, id_u integer, name text, description text, photo_path_list text, position_list text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
create table if not exists comments(id_c integer primary key autoincrement, id_p integer, id_u integer,comment text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
