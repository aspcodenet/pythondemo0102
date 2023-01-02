from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__= "Customer"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    City = db.Column(db.String(40), unique=False, nullable=False)
    TelephoneCountryCode = db.Column(db.Integer, unique=False, nullable=False)
    Telephone = db.Column(db.String(20), unique=False, nullable=False)