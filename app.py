from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from model import db, seedData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hejsan123@localhost/players0101'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        #seedData(db)
        app.run()
        while True:
            print("1. Create")
            print("2. List")        
            print("3. Exit")                
            action = input("Ange:")
            if action == "3":
                break
            if action == "1":
                print("Create")
            if action == "2":
                print("List")          
