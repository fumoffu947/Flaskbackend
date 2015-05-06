import requests,json
local_url ="http://flask-projekt.openshift.ida.liu.se/getuser"
data = json.dumps({'username':"test1","password":"test1","id_u":1})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/addfriend"
data = json.dumps({'username':"test1","password":"test1","id_u_friend":2})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/delete/removefriend"
data = json.dumps({'username':"test1","password":"test1","id_u_friend":2})
result = requests.post(local_url,data)
print(result)
print(result.text)

local_url ="http://flask-projekt.openshift.ida.liu.se/addfriend"
data = json.dumps({'username':"test1","password":"test1","id_u_friend":2})
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
