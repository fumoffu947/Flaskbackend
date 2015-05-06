import requests,json
local_url ="http://127.0.0.1:5000/getuser"
data = json.dumps({'id_u':1})
#result = requests.post(local_url,data)
#print(result)
#print(result.json())

name = "test1"
lastname = "testson1"
epost = "test1@hotmail.com"
username = "test1"
pasword = "test1"
data = json.dumps({"name":name,"lastname":lastname,"epost":epost,"username":username,"pasword":pasword})
local_url ="http://127.0.0.1:5000/adduser"
#result = requests.post(local_url,data)
#print(result)
#print(result.json())
