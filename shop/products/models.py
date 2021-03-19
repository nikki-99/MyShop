from shop import db
from datetime import datetime
from shop.customers.models import Customer



class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price= db.Column(db.Integer, nullable= False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable = False)
    
    description = db.Column(db.Text, nullable=False)
    adding_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    

    
    image_1 = db.Column(db.String(120), nullable = False, default='image.jpg')
    image_2 = db.Column(db.String(120), nullable = False, default='image.jpg')
    image_3 = db.Column(db.String(120), nullable = False, default='image.jpg')
    image_4 = db.Column(db.String(120), nullable = False, default='image.jpg')
    reviews = db.relationship('Review', backref = 'article', lazy = True, cascade="all,delete")

    



    def __repr__(self):
        return '<Addproduct %r>' % self.name


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    body =db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Numeric(2, 1),default = 0)
    timestamp = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('addproduct.id'),nullable = False)
