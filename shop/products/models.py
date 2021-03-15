from shop import db
from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
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


    def __repr__(self):
        return '<Addproduct %r>' % self.name

