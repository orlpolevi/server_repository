import requests

BASE = "http://127.0.0.1:5000/"

#respone = requests.post(BASE+"testing parser", data={'name': "testpost",'age':"29"})
#print(respone.json())

#respone = request.get(BASE+"hello")
#print(respone.json())


#respone = requests.post(BASE+"register", data={'name': "test_user_add",'lastname':"postrequest",
# 'password':"12345", 'gender':"maleish", 'email':"something@some.com", 'phone':"05444444"})
#print(respone.json())

respone = requests.post(BASE+"activate_GA", data={'name': "Michael", 'course':"mishdif"})
print(respone.json())