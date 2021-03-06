from shop import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# helps to convert dict to str..vice versa

@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(int(user_id))


class Customer(db.Model, UserMixin):
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





    def get_token(self, expires_sec = 1500):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    # no self parameter 
    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Customer.query.get(user_id) 

    def __repr__(self):
        return '<Customer %r>' % self.username 



class jsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)                

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    invoice = db.Column(db.String(15), unique = True, nullable=False)
    status = db.Column(db.String(50), nullable = False, default = 'Pending')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    orders = db.Column(jsonEncodedDict)


    def __repr__(self):
        return '<Order %r>' % self.invoice


