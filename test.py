import requests,json
local_url ="http://flask-projekt.openshift.ida.liu.se/user"
data = json.dumps({'id_u':1})
result = requests.post(local_url,data)
print(result)
