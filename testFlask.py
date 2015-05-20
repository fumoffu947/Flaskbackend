import os,json
import server as flaskr
import config
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE_PATH'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.apps = flaskr.app.test_client()
        config.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE_PATH'])

    def test_empty_db(self):
        rv = self.apps.get('/')
        assert "Hello World!" in rv.data

    def test_add_user(self):
        rv = self.apps.post('/adduser',data=self.get_user_data_1(), follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post('/adduser',data=self.get_user_data_1(), follow_redirects=True)
        assert "emailError" in rv.data
        rv = self.apps.post('/adduser',data=self.get_user_data_1_same_username(), follow_redirects=True)
        print(rv.data)
        assert "usernameExistsError" in rv.data


    def test_get_user(self):
        rv = self.apps.post('/adduser',data=self.get_user_data_1(), follow_redirects=True)
        assert "user added" in rv.data
        data_p = json.dumps({"id_u":1})
        rv = self.apps.post("/getuser",data=data_p,follow_redirects=True)
        assert "test1" in rv.data
        assert "testson1" in rv.data
        assert "test1@hotmail.com" in rv.data

    def test_post_path(self):
        rv = self.apps.post('/adduser',data=self.get_user_data_1(), follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/postpath",data=self.get_post_data_1(), follow_redirects=True)
        assert "post added" in rv.data
        
    def test_get_user_post(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/postpath",data=self.get_post_data_1(), follow_redirects=True)
        assert "post added" in rv.data
        rv = self.apps.post("/getuserpost",data=self.get_user_pas_1(),follow_redirects=True)
        assert "post test" in rv.data
        assert "this is a post test" in rv.data
        assert "[[50,70],[51,70]]" in rv.data

    def test_get_user_post_with_comments_and_likes(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/postpath",data=self.get_post_data_1(), follow_redirects=True)
        assert "post added" in rv.data        
        rv = self.apps.post("/postcomment", data=self.get_comment_data_1(), follow_redirects=True)
        assert "comment was added to post" in rv.data
        rv = self.apps.post("/addremovelike", data=self.get_like_data_1(), follow_redirects=True)
        print(rv.data)
        assert "post was liked" in rv.data
        rv = self.apps.post("/addremovelike", data=self.get_like_data_1(), follow_redirects=True)
        assert "post like was removed" in rv.data
        rv = self.apps.post("/addremovelike", data=self.get_invalid_like_data_1(), follow_redirects=True)
        print(rv.data)
        assert "invalidInput" in rv.data
        rv = self.apps.post("/getuserpost",data=self.get_user_pas_1(),follow_redirects=True)
        print(rv.data)
        assert "post test 1" in rv.data
        assert "this is a post test 1" in rv.data
        assert "[[50,70],[51,70]]" in rv.data
        assert "a comment on a post" in rv.data
        assert "test1" in rv.data
        assert "testson1" in rv.data
        assert "0" in rv.data

    def test_add_get_friends(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/adduser",data=self.get_user_data_2(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/addremovefriend",data=self.get_friend_data_1(), follow_redirects=True)
        assert "friend was added" in rv.data
        rv = self.apps.post("/getfriends",data=self.get_user_pas_1(), follow_redirects=True)
        assert "2" in rv.data
        assert "test2" in rv.data
        assert "testson2" in rv.data

    def test_add_remove_friend(self):
        rv = self.apps.post("/addremovefriend",data=self.get_friend_data_1(), follow_redirects=True)
        assert "friend was added" in rv.data
        rv = self.apps.post("/addremovefriend",data=self.get_friend_data_1())
        assert "friend was removed" in rv.data
        
    def test_get_user_flow(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/adduser",data=self.get_user_data_2(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/addremovefriend",data=self.get_friend_data_1(), follow_redirects=True)
        assert "friend was added" in rv.data
        rv = self.apps.post("/postpath",data=self.get_post_data_1(), follow_redirects=True)
        assert "post added" in rv.data        
        rv = self.apps.post("/postcomment", data=self.get_comment_data_1(), follow_redirects=True)
        assert "comment was added to post" in rv.data
        rv = self.apps.post("/postpath",data=self.get_post_data_2(), follow_redirects=True)
        assert "post added" in rv.data
        rv = self.apps.post("/getuserflowpost",data=self.get_user_pas_1(),follow_redirects=True)
        assert "post test 2" in rv.data
        assert "this is a post test 2" in rv.data
        rv = self.apps.post("/getuserflowpost",data=self.get_user_pas_2(),follow_redirects=True)
        assert "post test 1" in rv.data
        assert "this is a post test 1" in rv.data

    def test_login(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        data_out = json.dumps({"username":"test1","password":"test1"})
        rv = self.apps.post("/login", data=data_out, follow_redirects=True)
        assert "1" in rv.data
        data_out = json.dumps({"username":"feluser","password":"test1"})
        rv = self.apps.post("/login", data=data_out, follow_redirects=True)
        assert "usernameError" in rv.data
        data_out = json.dumps({"username":"test1","password":"felpass"})
        rv = self.apps.post("/login", data=data_out, follow_redirects=True)
        assert "passwordError" in rv.data

    def test_get_all(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.get("/test/getall")
        print(rv.data)
        assert "test1" in rv.data
        assert "testson1" in rv.data

    def test_search_users(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/adduser",data=self.get_user_data_2(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/searchuser", data=self.get_user_search_data_1(), follow_redirects=True)
        print(rv.data)
        assert "test2" in rv.data
        assert "testson2" in rv.data
        assert "test1" not in rv.data
        rv = self.apps.post("/searchuser", data=self.get_user_search_data_2(), follow_redirects=True)
        assert "test2" in rv.data
        assert "testson2" in rv.data
        assert "test1" not in rv.data

    def test_add_remove_follow(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/adduser",data=self.get_user_data_2(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/addremovefollow", data=self.get_follow_data_1(), follow_redirects=True)
        assert "follow was added" in rv.data
        rv = self.apps.post("/addremovefollow", data=self.get_follow_data_1(), follow_redirects=True)
        assert "follow was removed" in rv.data

    def test_add_friend_request(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/adduser",data=self.get_user_data_2(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/addfriendrequest", data=self.get_request_friend_data_1(), follow_redirects=True)
        assert "friend request added" in rv.data
        rv = self.apps.post("/addfriendrequest", data=self.get_request_friend_data_1(), follow_redirects=True)
        assert "friend request already exists" in rv.data
        rv = self.apps.post("/addfriendrequest", data=self.get_request_friend_data_2(), follow_redirects=True)
        assert "friend request added" in rv.data
        rv = self.apps.post("/getfriendrequests", data=self.get_request_friend_data_1(), follow_redirects=True)
        assert "2" in rv.data
        assert "test2" in rv.data
        assert "testson2" in rv.data
        rv = self.apps.post("/getfriendrequests", data=self.get_request_friend_data_2(), follow_redirects=True)
        assert "1" in rv.data
        assert "test1" in rv.data
        assert "testson1" in rv.data
        rv = self.apps.post("/removefriendrequest", data=self.get_request_friend_data_1(), follow_redirects=True)
        assert "friend request was removed" in rv.data

    def test_add_get_message(self):
        rv = self.apps.post("/adduser",data=self.get_user_data_1(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/adduser",data=self.get_user_data_2(),follow_redirects=True)
        assert "user added" in rv.data
        rv = self.apps.post("/addmessage", data=self.get_message_data_1(), follow_redirects=True)
        assert "message added" in rv.data
        rv = self.apps.post("/addmessage", data=self.get_message_data_2(), follow_redirects=True)
        assert "message added" in rv.data
        rv = self.apps.post("/getmessages", data=self.get_message_data_1(), follow_redirects=True)
        assert "test message 1" in rv.data
        assert "test message 2" in rv.data
        rv = self.apps.post("/getmessages", data=self.get_message_data_2(), follow_redirects=True)
        assert "test message 1" in rv.data
        assert "test message 2" in rv.data

    def get_user_data_1(self):
        name = "test1"
        lastname = "testson1"
        epost = "test1@hotmail.com"
        username = "test1"
        pasword = "test1"
        return json.dumps({"name":name,"lastname":lastname,"email":epost,"username":username,"password":pasword})

    def get_user_data_1_same_username(self):
        name = "test1"
        lastname = "testson1"
        epost = "test@hotmail.com"
        username = "test1"
        pasword = "test1"
        return json.dumps({"name":name,"lastname":lastname,"email":epost,"username":username,"password":pasword})

    def get_user_search_data_1(self):
        partname = "tes"
        username = "test1"
        pasword = "test1"
        return json.dumps({"partusername":partname,"username":username,"password":pasword})

    def get_user_search_data_2(self):
        partname = "2"
        username = "test1"
        pasword = "test1"
        return json.dumps({"partusername":partname,"username":username,"password":pasword})

    def get_user_data_1_empty_email(self):
        name = "test1"
        lastname = "testson1"
        epost = ""
        username = "test1"
        pasword = "test1"
        return json.dumps({"name":name,"lastname":lastname,"email":epost,"username":username,"password":pasword})

    def get_user_pas_1(self):
        username = "test1"
        pasword = "test1"
        return json.dumps({"username":username,"password":pasword})

    def get_user_pas_2(self):
        username = "test2"
        pasword = "test2"
        return json.dumps({"username":username,"password":pasword})

    def get_user_data_2(self):
        name = "test2"
        lastname = "testson2"
        epost = "test2@hotmail.com"
        username = "test2"
        pasword = "test2"
        return json.dumps({"name":name,"lastname":lastname,"email":epost,"username":username,"password":pasword})

    def get_post_data_1(self):
        username = "test1"
        pasword = "test1"
        name = "post test 1"
        desc = "this is a post test 1"
        photos = "pic,pic"
        positions = "[[50,70],[51,70]]"
        return json.dumps({"username":username,"password":pasword,"name":name,"description":desc,"position_list":positions, "photos":photos})

    def get_post_data_2(self):
        username = "test2"
        pasword = "test2"
        name = "post test 2"
        desc = "this is a post test 2"
        photos = "pic,pic"
        positions = "[[50,70],[51,70]]"
        return json.dumps({"username":username,"password":pasword,"name":name,"description":desc,"position_list":positions,"photos":photos})

    def get_comment_data_1(self):
        username = "test1"
        pasword = "test1"
        id_p = 1
        comment = "a comment on a post"
        return json.dumps({"id_p":id_p,"username":username,"password":pasword,"comment":comment})

    def get_friend_data_1(self):
        username = "test1"
        password = "test1"
        friend = 2
        return json.dumps({"username":username,"password":password,"id_u_friend":friend})

    def get_follow_data_1(self):
        username = "test1"
        password = "test1"
        follow = 2
        return json.dumps({"username":username,"password":password,"id_u_follow":follow})

    def get_like_data_1(self):
        username = "test1"
        pasword = "test1"
        id_p = 1
        return json.dumps({"username":username,"password":pasword,"id_p":id_p})

    def get_invalid_like_data_1(self):
        username = "test1"
        pasword = "test1"
        id_p = "troll"
        return json.dumps({"username":username,"password":pasword,"id_p":id_p})

    def get_request_friend_data_1(self):
        username = "test1"
        pasword = "test1"
        id_u_fr = 2
        return json.dumps({"username":username,"password":pasword,"id_u_fr":id_u_fr})

    def get_request_friend_data_2(self):
        username = "test2"
        pasword = "test2"
        id_u_fr = 1
        return json.dumps({"username":username,"password":pasword,"id_u_fr":id_u_fr})

    def get_message_data_1(self):
        username = "test1"
        pasword = "test1"
        id_u_to = 2
        message = "test message 1"
        return json.dumps({"username":username,"password":pasword,"id_u_to":id_u_to, "message":message})

    def get_message_data_2(self):
        username = "test2"
        pasword = "test2"
        id_u_to = 1
        message = "test message 2"
        return json.dumps({"username":username,"password":pasword,"id_u_to":id_u_to, "message":message})

if __name__ == '__main__':
    unittest.main()
