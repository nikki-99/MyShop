from shop import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    country = db.Column(db.String(120),  nullable=False)
    state = db.Column(db.String(120),  nullable=False)
    city = db.Column(db.String(120),  nullable=False)
    address = db.Column(db.String(120),  nullable=False)
    pin = db.Column(db.String(120),  nullable=False)
    contact= db.Column(db.String(120),  nullable=False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username 