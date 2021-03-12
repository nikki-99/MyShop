from shop import db
from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(80), nullable=False)
    price= db.Column(db.Numeric(10,2), nullable= False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable = False)
    colors = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    
    image_1 = db.Column(db.String(120), nullable = False, default='image.jpg')
    image_2 = db.Column(db.String(120), nullable = False, default='image.jpg')
    image_3 = db.Column(db.String(120), nullable = False, default='image.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(50), nullable=False, unique=True)