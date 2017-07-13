from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://diognhexsqognq:aa18612b2b57045a7b3f58942999b754dc4c2f55db9c6d47691a435505381124@ec2-184-73-199-72.compute-1.amazonaws.com:5432/devo8ico0tbo2l'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
