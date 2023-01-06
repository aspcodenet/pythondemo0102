from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from model import db, seedData, Customer

# gör om kontaktsida -> kundlist-sida (/Customers) - dvs byt namn på funktion, byt URL
# gör om Kundlist-sidan så du har en TEMPLATE (det finns en index copy.html 
#                  du kan kolla på så ser du ett exempel på loop)
# Kundlist-sidan ska ha en snygg TABLE
# Varje kund har en bild den bildens url ska vara https://img.systementor.se/<id>/300/200 - id är kundens id i databasen (numeriskt!)
# Vid klick på en BILD ska man komma till en Bild-sida
# På Bild-sidan ska NAMN + bild visas https://img.systementor.se/<id>/800/600
# I Kundlist-sidans tabell ska det vara en LÄNK -> Kundsida
# På Kundsidan visas ALL INFORMATION OM KUNDEN samt en bild https://img.systementor.se/<id>/500/400

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hejsan123@localhost/players0101'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

@app.route("/")
def startpage():
	    return render_template("index.html" )

@app.route("/customerimage/<id>")
def customerimagepage(id):
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("customerimage.html", customer=customer )


@app.route("/customer/<id>")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("customer.html", customer=customer )



@app.route("/customers")
def customerspage():
    #listOfCustomers = Customer.query.all()
    return render_template("customers.html", listOfCustomers=Customer.query.all() )

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
