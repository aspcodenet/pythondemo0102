from flask import Flask, render_template, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from random import randint
from flask_security import roles_accepted, auth_required, logout_user

from model import db, seedData, Customer
from person import PersonRegister, Person

from forms import NewCustomerForm, WithdrawForm
import os
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hejsan123@localhost/players01022'
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
db.app = app 
db.init_app(app)
migrate = Migrate(app,db)


@app.route("/api/customers")
def customers():
    customers=[]
    page = int(request.args.get('page',1))
    custs = Customer.query.order_by(Customer.Id.desc()).paginate(page=page,per_page=10    )
    for cust in custs.items:
        c = { "Id": cust.Id,"Name":cust.Name, "City":cust.City }
        customers.append(c)
    return jsonify(customers)

@app.route("/morecustomers")
def morecustomerspage():
    return render_template("morecustomers.html")

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

@app.route("/customers")
def customerspage():
    return render_template("customers.html",
                            customers=Customer.query.all())

@app.route("/withdraw/<int:id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def withdraw(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = WithdrawForm()

    ownValidationOk = True
    if request.method == 'POST':
        # todo Lägg till validering mot databas 
        # if form.amount.data > customer.amount 
        # GENERERA FEL
        form.amount.errors = form.amount.errors + ('Belopp to large',)
        ownValidationOk = False


    if ownValidationOk and form.validate_on_submit():
        customer.Amount = customer.Amount - form.amount.data
        # insert into transactions
        db.session.commit()

        # todo ändra i databasen
        #return redirect("/customer/" + str(id))
        return redirect("/customers")
    return render_template("withdraw.html", formen=form, customer=customer )



@app.route("/editcustomer/<int:id>", methods=['GET', 'POST'])
def editcustomer(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = NewCustomerForm()
    # if customer.Belopp < form.Belopp:        
    #     form.Belopp.errors = form.Belopp.errors + ('Belopp to large',)


    if form.validate_on_submit():
        #spara i databas
        customer.Name = form.name.data
        customer.City = form.city.data
        db.session.commit()
        return redirect("/customers" )
    if request.method == 'GET':
        form.name .data = customer.Name
        form.city.data = customer.City
    return render_template("editcustomer.html", formen=form )


@app.route("/newcustomer", methods=['GET', 'POST'])
def newcustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.Name = form.name.data
        customer.City = form.city.data
        customer.TelephoneCountryCode = 1
        customer.Telephone = "321323"
        customer.Amount = 0
        db.session.add(customer)
        db.session.commit()
        return redirect("/customers" )
    return render_template("newcustomer.html", formen=form )
    

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
    
        seedData(app,db)
        app.run(debug=True)
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
