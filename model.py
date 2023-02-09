import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_security import hash_password
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla

db = SQLAlchemy()


fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass

class User(db.Model, fsqla.FsUserMixin):
    pass

user_datastore = SQLAlchemyUserDatastore(db, User, Role)



class Customer(db.Model):
    __tablename__= "Customer"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    City = db.Column(db.String(40), unique=False, nullable=False)
    TelephoneCountryCode = db.Column(db.Integer, unique=False, nullable=False)
    Telephone = db.Column(db.String(20), unique=False, nullable=False)
    Amount = db.Column(db.Integer, unique=False, nullable=False)


def seedData(app,db):

    app.security = Security(app, user_datastore)
    app.security.datastore.db.create_all()
    if not app.security.datastore.find_role("Admin"):
        app.security.datastore.create_role(name="Admin")
    if not app.security.datastore.find_role("Staff"):
        app.security.datastore.create_role(name="Staff")
    if not app.security.datastore.find_user(email="admin@systementor.se"):
        app.security.datastore.create_user(email="admin@systementor.se", password=hash_password("password"),roles=["Admin"])
    if not app.security.datastore.find_user(email="worker1@systementor.se"):
        app.security.datastore.create_user(email="worker1@systementor.se", password=hash_password("password"),roles=["Staff"])
    if not app.security.datastore.find_user(email="worker2@systementor.se"):
        app.security.datastore.create_user(email="worker2@systementor.se", password=hash_password("password"),roles=["Staff"])
    app.security.datastore.db.session.commit()

    cites = ["Stockholm","Västerås", "Södertälje"]
    countrycodes = [46,47,44]
    antal =  Customer.query.count()
    while antal < 100:
        customer = Customer()
        customer.Name = "Customer" + str(antal)
        customer.TelephoneCountryCode = random.choice(countrycodes)
        customer.Telephone = random.randint(10000000,999999999)
        customer.City = random.choice(cites)
        customer.Amount = 0
        db.session.add(customer)
        db.session.commit()
        antal = antal + 1
