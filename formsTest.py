import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app
from model import db, Customer, User,Role
from flask_security import Security,SQLAlchemyUserDatastore, hash_password
from sqlalchemy import create_engine


def set_current_user(app, ds, email):
    """Set up so that when request is received,
    the token will cause 'user' to be made the current_user
    """

    def token_cb(request):
        if request.headers.get("Authentication-Token") == "token":
            return ds.find_user(email=email)
        return app.security.login_manager.anonymous_user()

    app.security.login_manager.request_loader(token_cb)


init = False

class FormsTestCases(unittest.TestCase):
    # def __init__(self, *args, **kwargs):
    #     super(FormsTestCases, self).__init__(*args, **kwargs)
    def tearDown(self):
        self.ctx.pop()
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        #self.client = app.test_client()
        app.config["SERVER_NAME"] = "stefan.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SECURITY_FRESHNESS_GRACE_PERIOD'] = 123454
        global init
        if not init:
            db.init_app(app)
            db.create_all()
            init = True
            user_datastore = SQLAlchemyUserDatastore(db, User, Role)
            app.security = Security(app, user_datastore,register_blueprint=False)
            app.security.init_app(app, user_datastore,register_blueprint=False)
            app.security.datastore.db.create_all()




   


    def test_when_withdrawing_more_than_balance_should_show_errormessage(self):
        # arrangera världen så att kund med id 1 har amount 100
        # ta ut 200
        # kolla i rerultat HTML = "Belopp to large"

        # app.security.datastore.create_role(name="Admin")
        # app.security.datastore.create_user(email="unittest@me.com", password=hash_password("password"), roles=["Admin"])
        # app.security.datastore.commit()

        # set_current_user(app, app.security.datastore, "unittest@me.com")


        customer = Customer()
        customer.Name = "Stefan"
        customer.TelephoneCountryCode = "1223"
        customer.Telephone = "12343"
        customer.City = "Test"
        customer.Amount = 100
        db.session.add(customer)
        db.session.commit()

        test_client = app.test_client()
        user = User.query.get(1)
        with test_client:
            url = '/withdraw/' + str(customer.Id)
            response = test_client.post(url, data={ "amount":"200"})
            s = response.data.decode("utf-8") 
            ok = 'Belopp to large' in s
            self.assertTrue(ok)


    def test_when_creating_new_should_validate_name_ends_with_se(self):
        test_client = app.test_client()
        with test_client:
            url = '/newcustomer'
            response = test_client.post(url, data={ "name":"Kalle", "city":"Teststad", "age":"31", "countryCode":"SE", "Amount":"0" }, headers={app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"]: "token"} )
            s = response.data.decode("utf-8") 
            ok = 'Måste sluta på .se dummer' in s
            self.assertTrue(ok)

    def test_when_creating_new_should_be_ok_when_name_is_ok(self):
        test_client = app.test_client()
        with test_client:
            url = '/newcustomer'
            response = test_client.post(url, data={ "name":"Kalle.se", "city":"Teststad", "age":"12", "countryCode":"SE", "Amount":"0" },headers={app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"]: "token"} )
            self.assertEqual('302 FOUND', response.status)




if __name__ == "__main__":
    unittest.main()