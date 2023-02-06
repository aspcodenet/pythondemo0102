import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app
from model import db, Customer

from sqlalchemy import create_engine


class FormsTestCases(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PersonerTestCases, self).__init__(*args, **kwargs)
        self.ctx = app.app_context()
        self.ctx.push()
        #self.client = app.test_client()
        app.config["SERVER_NAME"] = "stefan.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        db.init_app(app)
        db.app = app
        db.create_all()

    def tearDown(self):
        #self.ctx.pop()
        pass

    def test_when_creating_new_should_validate_name_is_longer_than_three(self):
        test_client = app.test_client()
        with test_client:
            url = '/newcustomer'
            response = test_client.post(url, data={ "name":"Kalle", "city":"Teststad", "age":"12", "countryCode":"SE" })
            s = response.data.decode("utf-8") 
            ok = 'Måste sluta på .se dummer' in s
            self.assertTrue(ok)

    def test_when_creating_new_should_be_ok_when_name_is_longer_than_three(self):
        test_client = app.test_client()
        with test_client:
            url = '/newcustomer'
            response = test_client.post(url, data={ "name":"Kalle.se", "city":"Teststad", "age":"12", "countryCode":"SE" })
            self.assertEqual('302 FOUND', response.status)




if __name__ == "__main__":
    unittest.main()