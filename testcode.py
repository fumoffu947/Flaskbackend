import os
import unittest
from flask import json, Flask
 
from config import basedir
from api import app, db
 
from flask.ext.testing import TestCase
 
from api import app, db
 
class RestTest(TestCase):
    """Unittest for API routes contained in api_routes.py"""
    
    def create_app(self):
        """Required method. Always implement this so that app is returned with context."""
        app.config['TESTING'] = True
        app.config['DATABASE_PATH'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False # This must be disabled for post to succeed during tests
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        return app
    
    def setUp(self):
        """Orders sqlalchemy to set up an test database"""
        db.create_all()

    @app.teardown_appcontext
    def tearDown(self):
        """Order sqlalchemy to drop all tables in test database"""
        db.session.remove()
        db.drop_all()

    def test_new_user(self):
        """Tests user creation"""

        base_url = 'http://flask-projekt.openshift.ida.liu.se/'

        # create a user
        username = 'foo'
        password = 'bar'

        data = json.dumps({'username': username, 'password': password})
        resp = self.client.post(base_url + '/users', data=data)
        self.assertTrue(resp.status_code == 201) # Successful creation
 
if __name__ == '__main__':
    unittest.main() 
