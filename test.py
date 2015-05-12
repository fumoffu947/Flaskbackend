import requests,json

local_url ="http://flask-projekt.openshift.ida.liu.se/adduser"
data = json.dumps({'username':"ph","password":"ph","lastname":"Johansson","name":"Philip","email":"email"})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/adduser"
data = json.dumps({'username':"test1","password":"test1","lastname":"testson","name":"test1","email":"testmail"})
result = requests.post(local_url,data)
print(result)
print(result.text)


local_url ="http://flask-projekt.openshift.ida.liu.se/adduser"
data = json.dumps({'username':"t","password":"t","lastname":"tson","name":"t","email":"tmail"})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/getuser"
data = json.dumps({'username':"test1","password":"test1","id_u":4})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/addfriend"
data = json.dumps({'username':"test1","password":"test1","id_u_friend":3})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/delete/removefriend"
data = json.dumps({'username':"test1","password":"test1","id_u_friend":3})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/addfriend"
data = json.dumps({'username':"test1","password":"test1","id_u_friend":3})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/postpath"
data = json.dumps({'username':"ph","password":"ph","name":"a path","description":"en forklaring","position_list":"[[]]"})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/postpath"
data = json.dumps({'username':"test1","password":"test1","name":"test1 path","description":"it is so funna when thisng word you know that is nice","position_list":"[[]]"})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/addfriend"
data = json.dumps({'username':"ph","password":"ph","id_u_friend":2})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/addfriend"
data = json.dumps({'username':"ph","password":"ph","id_u_friend":3})
result = requests.post(local_url,data)
print(result)
print(result.text)

name = "test1"
lastname = "testson1"
epost = "test1@hotmail.com"
username = "test1"
pasword = "test1"
data = json.dumps({"name":name,"lastname":lastname,"epost":epost,"username":username,"password":pasword})
local_url =""
#result = requests.post(local_url,data)
#print(result)
#print(result.json())
