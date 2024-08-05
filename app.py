from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Connect Flask API/app to database BEFORE creating db object... DBMS, DB_DRIVER, DB_USER, DB_PASS, URL, PORT, DB_NAME:
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://my_user:password1@localhost:5432/my_flask_db"

# Create database object AFTER configuring app / connecting API to DB::
db = SQLAlchemy(app)

# Create Marshmallow object:
ma = Marshmallow(app)


# Create a general class/model [MVC] of a table (this is how you define a model/table):
# No need to __init__ bc of inheritance:


class Service(db.Model):
    # Define table name:
    __tablename__ = "services"

    # Define PK object [Column is also a class]:
    id = db.Column(db.Integer, primary_key=True)

    # Define other attributes:
    name = db.Column(db.String(100), nullable=False)
    # No string length limit for description:
    description = db.Column(db.String)
    price = db.Column(db.Float)
    duration = db.Column(db.Integer)

# ^^ up to this point (and also maybe more after? idk) we're working with DDL... "definition" language ^^

# Create a marshmallow schema to convert SQL to python (this is how you access above table / fetch info from the DB):


class ServiceSchema(ma.Schema):
    class Meta:
        # Fields tuple:
        fields = ("id", "name", "description", "price", "duration")


# Now need to create object of class ServiceSchema. There are two ways... 1) To handle multiple/all tables?/services:
services_schema = ServiceSchema(many=True)

# 2) To handle a single service:
service_schema = ServiceSchema()


# Custom CLI commands:
# This is to enable typing "flask create" into the terminal (must be connected to correct db first, i.e. command prompt my_flask_db=#):
# This is a controller/s (MVC)?:


@app.cli.command("create")
def create_tables():
    # We've only create one table (Service) but in reality we'd have more:
    db.create_all()
    print("Create all the tables")


# Create another command to seed values to the table:
@app.cli.command("seed")
def seed_tables():
    # To create a service object, there's two ways:
    # Option 1:
    service1 = Service(
        name="Landscaping",
        description="Mow entire lawn",
        price=99.99,
        duration=1
    )

    # Option 2:
    service2 = Service()
    service2.name = "Renovation"
    service2.description = "Rework entire kitchen"
    service2.price = 5999.99
    service2.duration = 7

    # Another way... could use this instead of the below (adding all things at once):
    # services = [service1, service2]
    # db.session.add_all(services)

    # Analogous to Git... Add to session (adding specific things individually... maybe less elegant):
    db.session.add(service1)
    db.session.add(service2)

    # Analogous to Git... Commit to session/database:
    db.session.commit()

    print("Tables seeded.")

# Drop (delete) tables:


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped successfully.")


# Working with routes:
# Define routes (if methods=[""] is unspecified, it defaults to GET method):
# Static routing:
@app.route("/services")
def get_services():
    # Need to convert SQL/HTTP? requests to/with python, send to database, fetch, convert/translate outcome and display:
    # SELECT * FROM services;:

    # need to define a stmt (statement) that i'll be executing:
    # it's a statement object that represents the query itself:

    stmt = db.select(Service)

    # to execute stmt, we need to define another variable to store result in? as scalar/s:
    # Multiple "services" and "scalars", not singular:
    services_list = db.session.scalars(stmt)
    # Serialisation / and convert for python to understand using the "multiple services" version:
    data = services_schema.dump(services_list)
    return data

# Used this to troubleshoot localhost working and 127.0.0.1 not working:
# print("app.url_map:", app.url_map)

# Orrrr Dynamic routing... use <>, the contents of which is gotten from the frontend:


@app.route("/services/<int:service_id>")
# e.g. localhost/services/100
def get_service(service_id):
    # SELECT * FROM services WHERE id = service_id;:
    # In SQLAlchemy, can also use filter() instead of filter_by():
    stmt = db.select(Service).filter_by(id=service_id)
    # ^^ id is from backend; service_id is from frontend ^^

    # Execute stmt using scalar method/value; Singular "service" and "scalar", not multiple:
    service = db.session.scalar(stmt)

    # converting from db object to python object:
    # if service exists:
    if service:
        data = service_schema.dump(service)
        return data
    else:
        return {"error": f"Service with id {service_id} does not exist"}, 404


# RECAP:
# /services, GET => getting all services
# /services/id, GET => get a specific service
# /services, POST => Adding a service
# /services/id, PUT/PATCH => Edit a service
# /services/id, DELETE => Delete a specific service
