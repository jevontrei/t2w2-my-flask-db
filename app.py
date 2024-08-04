from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect Flask API/app to database = DBMS, DB_DRIVER, DB_USER, DB_PASS, URL, PORT, DB_NAME:
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://my_user:password1@localhost:5432/my_flask_db"

# Create object:
db = SQLAlchemy(app)

# Create a general class/model [MVC] of a table (this is how you define table):
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
    stock = db.Column(db.Integer)


# Custom CLI commands:
