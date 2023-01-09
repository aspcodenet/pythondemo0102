from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from random import randint

from model import db, seedData, Customer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:stefan@localhost/players0101'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

@app.route("/")
def startpage():
    dagen = "Måndag"
    siffran = randint(1,6)
   

    html = render_template("index.html", 
                            dag=dagen,
                            siffran=siffran,
                            customers=Customer.query.all()
    )
    return html

	    #return "<h1>test</h1>"
        # <html><head></head><</html>

@app.route("/kontakt")
def contactpage():
    s = "<html><head><title>Get lost</title></head><body>"
    for c in Customer.query.all():
        s = s + c.Name + "<br />"
    s = s + "</body></html>"
    return s

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        seedData(db)
        app.run()
        # while True:
        #     print("1. Create")
        #     print("2. List")        
        #     print("3. Exit")                
        #     action = input("Ange:")
        #     if action == "3":
        #         break
        #     if action == "1":
        #         print("Create")
        #     if action == "2":
        #         print("List")          
